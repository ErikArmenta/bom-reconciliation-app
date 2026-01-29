"""
BOM Comparator Module - BOM Reconciliation Application
Compares BOMs and generates status reports
Author: Master Engineer Erik Armenta
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from difflib import SequenceMatcher

from config import QUANTITY_TOLERANCE, STATUS_ICONS, STATUS_LABELS


def normalize_unit(unit: str) -> str:
    """
    Normalize unit of measure for comparison.
    
    Args:
        unit: Unit string
        
    Returns:
        Normalized unit string
    """
    if pd.isna(unit):
        return ""
    
    unit_str = str(unit).strip().upper()
    
    # Common unit normalizations
    unit_mappings = {
        'PCS': ['PCS', 'PC', 'PIECE', 'PIECES', 'PZA', 'PZAS', 'PIEZA', 'PIEZAS'],
        'KG': ['KG', 'KILOGRAM', 'KILOGRAMS', 'KILO', 'KILOS'],
        'M': ['M', 'METER', 'METERS', 'METRO', 'METROS'],
        'L': ['L', 'LITER', 'LITERS', 'LITRO', 'LITROS'],
        'G': ['G', 'GRAM', 'GRAMS', 'GRAMO', 'GRAMOS'],
        'CM': ['CM', 'CENTIMETER', 'CENTIMETERS', 'CENTIMETRO', 'CENTIMETROS'],
        'MM': ['MM', 'MILLIMETER', 'MILLIMETERS', 'MILIMETRO', 'MILIMETROS'],
        'FT': ['FT', 'FOOT', 'FEET', 'PIE', 'PIES'],
        'IN': ['IN', 'INCH', 'INCHES', 'PULGADA', 'PULGADAS'],
        'LB': ['LB', 'POUND', 'POUNDS', 'LIBRA', 'LIBRAS'],
    }
    
    for standard_unit, variations in unit_mappings.items():
        if unit_str in variations:
            return standard_unit
    
    return unit_str


def validate_quantity(qty1, qty2, tolerance: float = QUANTITY_TOLERANCE) -> bool:
    """
    Validate if two quantities match within tolerance.
    
    Args:
        qty1: First quantity
        qty2: Second quantity
        tolerance: Acceptable difference percentage
        
    Returns:
        True if quantities match within tolerance
    """
    try:
        q1 = float(qty1) if not pd.isna(qty1) else 0.0
        q2 = float(qty2) if not pd.isna(qty2) else 0.0
        
        if q1 == 0 and q2 == 0:
            return True
        
        if q1 == 0 or q2 == 0:
            return False
        
        diff_pct = abs(q1 - q2) / max(q1, q2)
        return diff_pct <= tolerance
        
    except (ValueError, TypeError):
        return str(qty1).strip() == str(qty2).strip()


def validate_unit(unit1, unit2) -> bool:
    """
    Validate if two units of measure match.
    
    Args:
        unit1: First unit
        unit2: Second unit
        
    Returns:
        True if units match
    """
    norm1 = normalize_unit(unit1)
    norm2 = normalize_unit(unit2)
    
    return norm1 == norm2


def validate_description(desc1, desc2, threshold: float = 0.8) -> bool:
    """
    Validate if two descriptions are similar enough.
    
    Args:
        desc1: First description
        desc2: Second description
        threshold: Minimum similarity threshold
        
    Returns:
        True if descriptions are similar
    """
    if pd.isna(desc1) and pd.isna(desc2):
        return True
    
    if pd.isna(desc1) or pd.isna(desc2):
        return False
    
    str1 = str(desc1).strip().lower()
    str2 = str(desc2).strip().lower()
    
    if str1 == str2:
        return True
    
    similarity = SequenceMatcher(None, str1, str2).ratio()
    return similarity >= threshold


def compare_boms(
    df_sap: pd.DataFrame,
    df_software_b: pd.DataFrame,
    mapping_sap: Dict,
    mapping_software_b: Dict
) -> pd.DataFrame:
    """
    Compare two BOMs and generate reconciliation report.
    
    Args:
        df_sap: SAP BOM DataFrame
        df_software_b: Software B BOM DataFrame
        mapping_sap: Column mapping for SAP
        mapping_software_b: Column mapping for Software B
        
    Returns:
        DataFrame with comparison results
    """
    # Get column names from mappings
    sap_part_col = mapping_sap['part_number']['column']
    sap_qty_col = mapping_sap['quantity']['column']
    sap_unit_col = mapping_sap['unit']['column']
    sap_desc_col = mapping_sap['description']['column']
    
    sb_part_col = mapping_software_b['part_number']['column']
    sb_qty_col = mapping_software_b['quantity']['column']
    sb_unit_col = mapping_software_b['unit']['column']
    sb_desc_col = mapping_software_b['description']['column']
    
    # Create result DataFrame
    results = []
    
    # Get all unique part numbers
    sap_parts = set(df_sap[sap_part_col].astype(str).str.strip())
    sb_parts = set(df_software_b[sb_part_col].astype(str).str.strip())
    all_parts = sap_parts.union(sb_parts)
    
    for part in all_parts:
        # Get rows for this part number
        sap_row = df_sap[df_sap[sap_part_col].astype(str).str.strip() == part]
        sb_row = df_software_b[df_software_b[sb_part_col].astype(str).str.strip() == part]
        
        result = {'Part Number': part}
        
        # Determine status
        if sap_row.empty and not sb_row.empty:
            # Missing in SAP
            status = 'missing_sap'
            result['Status'] = f"{STATUS_ICONS[status]} {STATUS_LABELS[status]}"
            result['SAP Quantity'] = None
            result['SAP Unit'] = None
            result['SAP Description'] = None
            result['Software B Quantity'] = sb_row.iloc[0][sb_qty_col] if sb_qty_col else None
            result['Software B Unit'] = sb_row.iloc[0][sb_unit_col] if sb_unit_col else None
            result['Software B Description'] = sb_row.iloc[0][sb_desc_col] if sb_desc_col else None
            result['Issues'] = 'Material no existe en SAP'
            
        elif sb_row.empty and not sap_row.empty:
            # Missing in Software B
            status = 'missing_software_b'
            result['Status'] = f"{STATUS_ICONS[status]} {STATUS_LABELS[status]}"
            result['SAP Quantity'] = sap_row.iloc[0][sap_qty_col] if sap_qty_col else None
            result['SAP Unit'] = sap_row.iloc[0][sap_unit_col] if sap_unit_col else None
            result['SAP Description'] = sap_row.iloc[0][sap_desc_col] if sap_desc_col else None
            result['Software B Quantity'] = None
            result['Software B Unit'] = None
            result['Software B Description'] = None
            result['Issues'] = 'Material no existe en Software B'
            
        else:
            # Exists in both - compare values
            sap_qty = sap_row.iloc[0][sap_qty_col] if sap_qty_col else None
            sap_unit = sap_row.iloc[0][sap_unit_col] if sap_unit_col else None
            sap_desc = sap_row.iloc[0][sap_desc_col] if sap_desc_col else None
            
            sb_qty = sb_row.iloc[0][sb_qty_col] if sb_qty_col else None
            sb_unit = sb_row.iloc[0][sb_unit_col] if sb_unit_col else None
            sb_desc = sb_row.iloc[0][sb_desc_col] if sb_desc_col else None
            
            result['SAP Quantity'] = sap_qty
            result['SAP Unit'] = sap_unit
            result['SAP Description'] = sap_desc
            result['Software B Quantity'] = sb_qty
            result['Software B Unit'] = sb_unit
            result['Software B Description'] = sb_desc
            
            # Check for discrepancies
            issues = []
            
            qty_match = validate_quantity(sap_qty, sb_qty)
            unit_match = validate_unit(sap_unit, sb_unit)
            desc_match = validate_description(sap_desc, sb_desc)
            
            if not qty_match:
                issues.append('Cantidad diferente')
            if not unit_match:
                issues.append('Unidad diferente')
            if not desc_match:
                issues.append('Descripción diferente')
            
            if issues:
                status = 'discrepancy'
                result['Status'] = f"{STATUS_ICONS[status]} {STATUS_LABELS[status]}"
                result['Issues'] = '; '.join(issues)
            else:
                status = 'correct'
                result['Status'] = f"{STATUS_ICONS[status]} {STATUS_LABELS[status]}"
                result['Issues'] = 'Todo correcto'
        
        results.append(result)
    
    # Create DataFrame from results
    df_results = pd.DataFrame(results)
    
    # Reorder columns
    column_order = [
        'Part Number', 'Status', 'Issues',
        'SAP Quantity', 'Software B Quantity',
        'SAP Unit', 'Software B Unit',
        'SAP Description', 'Software B Description'
    ]
    
    df_results = df_results[column_order]
    
    return df_results


def generate_status_report(df_comparison: pd.DataFrame) -> Dict[str, any]:
    """
    Generate summary statistics from comparison results.
    
    Args:
        df_comparison: Comparison results DataFrame
        
    Returns:
        Dictionary with summary statistics
    """
    total = len(df_comparison)
    
    correct = len(df_comparison[df_comparison['Status'].str.contains('Correcto', na=False)])
    discrepancies = len(df_comparison[df_comparison['Status'].str.contains('Discrepancia', na=False)])
    missing_sap = len(df_comparison[df_comparison['Status'].str.contains('Faltante en SAP', na=False)])
    missing_software_b = len(df_comparison[df_comparison['Status'].str.contains('Faltante en Software B', na=False)])
    
    total_issues = discrepancies + missing_sap + missing_software_b
    
    report = {
        'Total Materiales': total,
        'Correctos': correct,
        'Discrepancias': discrepancies,
        'Faltantes en SAP': missing_sap,
        'Faltantes en Software B': missing_software_b,
        'Total con Problemas': total_issues,
        'Porcentaje Correcto': round((correct / total * 100) if total > 0 else 0, 2),
        'Porcentaje con Problemas': round((total_issues / total * 100) if total > 0 else 0, 2)
    }
    
    return report
