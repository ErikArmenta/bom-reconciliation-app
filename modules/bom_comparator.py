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
        df_software_b: HPLM BOM DataFrame
        mapping_sap: Column mapping for SAP
        mapping_software_b: Column mapping for HPLM
        
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
    
    # Helper to prepare dataframe for comparison
    def prepare_df(df, part_col, qty_col, unit_col, desc_col, source_name):
        # Create a working copy
        work_df = df.copy()
        
        # Normalize unit for grouping
        if unit_col:
            work_df['__norm_unit'] = work_df[unit_col].apply(normalize_unit)
        else:
            work_df['__norm_unit'] = "UNASSIGNED"
            
        # Ensure quantities are numeric
        if qty_col:
            work_df[qty_col] = pd.to_numeric(work_df[qty_col], errors='coerce').fillna(0)
        
        # Aggregate quantities by Part and Unit
        # We take the first description found for the group
        agg_rules = {qty_col: 'sum'}
        if desc_col:
            agg_rules[desc_col] = 'first'
            
        # Group by Part and Normalized Unit
        grouped = work_df.groupby([part_col, '__norm_unit']).agg(agg_rules).reset_index()
        return grouped

    # Prepare both dataframes
    sap_grouped = prepare_df(df_sap, sap_part_col, sap_qty_col, sap_unit_col, sap_desc_col, "SAP")
    sb_grouped = prepare_df(df_software_b, sb_part_col, sb_qty_col, sb_unit_col, sb_desc_col, "HPLM")
    
    # Create result list
    results = []
    
    # Get all unique (Part, Unit) keys
    # Key format: (Part Number, Normalized Unit)
    sap_keys = set(zip(sap_grouped[sap_part_col].astype(str).str.strip(), sap_grouped['__norm_unit']))
    sb_keys = set(zip(sb_grouped[sb_part_col].astype(str).str.strip(), sb_grouped['__norm_unit']))
    all_keys = sap_keys.union(sb_keys)
    
    for part, norm_unit in all_keys:
        # Find rows in grouped dataframes
        sap_row = sap_grouped[
            (sap_grouped[sap_part_col].astype(str).str.strip() == part) & 
            (sap_grouped['__norm_unit'] == norm_unit)
        ]
        
        sb_row = sb_grouped[
            (sb_grouped[sb_part_col].astype(str).str.strip() == part) & 
            (sb_grouped['__norm_unit'] == norm_unit)
        ]
        
        result = {'Part Number': part}
        
        # Extract values
        sap_qty = sap_row.iloc[0][sap_qty_col] if not sap_row.empty else 0
        sap_desc = sap_row.iloc[0][sap_desc_col] if not sap_row.empty and sap_desc_col else ""
        # Keep original unit name if possible, otherwise use normalized
        # We can't easily get the original unit if we grouped, but strictly we grouped by normalized.
        # Let's try to get a representative unit from the original DF if needed, but for now use what we have?
        # Actually, we don't have the original unit column in grouped if it wasn't aggregated.
        # But we grouped by [part_col, '__norm_unit'], so we don't have the raw unit string unless we agg it.
        # For simplicity, let's use the normalized unit for display or "Mixed" if we really cared, 
        # but usually normalized is better for comparison.
        sap_unit_display = norm_unit if norm_unit != "UNASSIGNED" else ""

        sb_qty = sb_row.iloc[0][sb_qty_col] if not sb_row.empty else 0
        sb_desc = sb_row.iloc[0][sb_desc_col] if not sb_row.empty and sb_desc_col else ""
        sb_unit_display = norm_unit if norm_unit != "UNASSIGNED" else ""
        
        result['SAP Quantity'] = sap_qty if not sap_row.empty else None
        result['SAP Unit'] = sap_unit_display
        result['SAP Description'] = sap_desc
        result['HPLM Quantity'] = sb_qty if not sb_row.empty else None
        result['HPLM Unit'] = sb_unit_display
        result['HPLM Description'] = sb_desc
        
        # Logic: SAP is Master.
        # Difference = SAP - HPLM
        # > 0 implies SAP has more (so HPLM is missing/lacking => Falta en HPLM)
        # < 0 implies HPLM has more (so HPLM has surplus => Sobra en HPLM)
        # Wait, user said: "que diga falta o sobra segun sea el caso"
        # "Falta" usually means "Missing from the target (HPLM) compared to Source (SAP)".
        # "Sobra" usually means "Excess in target (HPLM) compared to Source (SAP)".
        
        difference = sap_qty - sb_qty
        
        # Tolerance check
        if abs(difference) <= (max(sap_qty, sb_qty) * QUANTITY_TOLERANCE) if max(sap_qty, sb_qty) > 0 else (sap_qty == sb_qty):
             status = 'correct'
             result['Status'] = f"{STATUS_ICONS[status]} {STATUS_LABELS[status]}"
             result['Issues'] = 'OK'
        else:
            if difference > 0:
                # SAP(10) - HPLM(8) = 2. Falta 2 en HPLM.
                status = 'falta'
                result['Status'] = f"{STATUS_ICONS[status]} {STATUS_LABELS[status]}"
                result['Issues'] = f"Falta {difference:g} en HPLM"
            else:
                # SAP(10) - HPLM(12) = -2. Sobra 2 en HPLM.
                status = 'sobra'
                result['Status'] = f"{STATUS_ICONS[status]} {STATUS_LABELS[status]}"
                result['Issues'] = f"Sobra {abs(difference):g} en HPLM"
        
        # Check description if strictly needed, but user emphasized quantity/part logic mainly.
        # We will ignore description mismatches for status to focus on "Falta/Sobra" as requested.
        
        results.append(result)
    
    # Create DataFrame from results
    df_results = pd.DataFrame(results)
    
    # Reorder columns
    column_order = [
        'Part Number', 'Status', 'Issues',
        'SAP Quantity', 'HPLM Quantity',
        'SAP Unit', 'HPLM Unit',
        'SAP Description', 'HPLM Description'
    ]
    
    # Ensure all columns exist
    for col in column_order:
        if col not in df_results.columns:
            df_results[col] = None
            
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
    falta = len(df_comparison[df_comparison['Status'].str.contains('Falta', na=False)])
    sobra = len(df_comparison[df_comparison['Status'].str.contains('Sobra', na=False)])
    
    total_issues = falta + sobra
    
    report = {
        'Total Materiales': total,
        'Correctos': correct,
        'Faltantes/Diferencias (-)': falta, # Using generic label for Falta
        'Sobrantes/Excedentes (+)': sobra,  # Using generic label for Sobra
        'Total con Problemas': total_issues,
        'Porcentaje Correcto': round((correct / total * 100) if total > 0 else 0, 2),
        'Porcentaje con Problemas': round((total_issues / total * 100) if total > 0 else 0, 2),
        # Keep keys for compatibility if needed, but updated values
        'Faltantes en SAP': 0, # Deprecated logic
        'Faltantes en Software B': falta, # Mapping "Falta" roughly here for old UI compatibility if needed
        'Discrepancias': sobra # Mapping "Sobra" roughly here
    }
    
    return report
    
    return report
