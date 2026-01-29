"""
Data Handler Module - BOM Reconciliation Application
Handles file loading with SAP padding preservation and Excel export
Author: Master Engineer Erik Armenta
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import re
from io import BytesIO
import xlsxwriter

from config import COLUMN_PATTERNS, SUPPORTED_FORMATS, EXCEL_SHEET_NAMES, COLORS


def detect_material_columns(df: pd.DataFrame) -> list:
    """
    Pre-inspection: Detect columns that likely contain material identifiers.
    Critical for preserving SAP padding (leading zeros).
    
    Args:
        df: DataFrame to inspect
        
    Returns:
        List of column names that are material identifiers
    """
    material_columns = []
    
    # Check column names against known patterns
    for col in df.columns:
        col_lower = str(col).lower().strip()
        
        # Check if column name matches material identifier patterns
        for pattern in COLUMN_PATTERNS['part_number']:
            if pattern in col_lower:
                material_columns.append(col)
                break
    
    return material_columns


def load_file(file, filename: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Load Excel or CSV file with intelligent dtype preservation.
    Preserves leading zeros in material identifiers (SAP padding).
    
    Args:
        file: File object from st.file_uploader
        filename: Name of the uploaded file
        
    Returns:
        Tuple of (DataFrame, error_message)
        If successful: (DataFrame, None)
        If error: (None, error_message)
    """
    try:
        file_ext = Path(filename).suffix.lower()
        
        if file_ext not in SUPPORTED_FORMATS:
            return None, f"Formato no soportado: {file_ext}. Use {', '.join(SUPPORTED_FORMATS)}"
        
        # First pass: Read with default types to detect material columns
        if file_ext in ['.xlsx', '.xls']:
            df_preview = pd.read_excel(file, nrows=5)
        else:
            df_preview = pd.read_csv(file, nrows=5)
        
        # Detect material identifier columns
        material_cols = detect_material_columns(df_preview)
        
        # Reset file pointer
        file.seek(0)
        
        # Second pass: Read with proper dtype preservation
        if file_ext in ['.xlsx', '.xls']:
            # Create converters dict to force string type for material columns
            converters = {col: str for col in material_cols}
            
            # Read with converters to preserve leading zeros
            df = pd.read_excel(file, converters=converters)
        else:
            # For CSV, use dtype parameter
            dtype_dict = {col: str for col in material_cols}
            df = pd.read_csv(file, dtype=dtype_dict)
        
        # Validate the loaded DataFrame
        if df.empty:
            return None, "El archivo está vacío"
        
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Strip whitespace from string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
        
        # Replace 'nan' strings with actual NaN
        df.replace('nan', np.nan, inplace=True)
        
        return df, None
        
    except Exception as e:
        return None, f"Error al cargar el archivo: {str(e)}"


def validate_dataframe(df: pd.DataFrame, source_name: str) -> Optional[str]:
    """
    Validate DataFrame has required structure.
    
    Args:
        df: DataFrame to validate
        source_name: Name of the data source (for error messages)
        
    Returns:
        Error message if validation fails, None if successful
    """
    if df is None or df.empty:
        return f"El DataFrame de {source_name} está vacío"
    
    if len(df.columns) == 0:
        return f"El DataFrame de {source_name} no tiene columnas"
    
    return None


def sanitize_cell_value(value):
    """
    Sanitize cell value for Excel export.
    Handles NaN, Inf, and None values.
    
    Args:
        value: Cell value to sanitize
        
    Returns:
        Safe value for Excel export
    """
    if pd.isna(value) or value is None:
        return ""
    if isinstance(value, (float, np.floating)):
        if np.isinf(value):
            return ""
        if np.isnan(value):
            return ""
    return value


def export_to_excel(
    df_all: pd.DataFrame,
    df_discrepancies: pd.DataFrame,
    df_summary: Dict[str, Any]
) -> BytesIO:
    """
    Export reconciliation results to formatted Excel file.
    
    Args:
        df_all: Complete reconciliation DataFrame
        df_discrepancies: DataFrame with only discrepancies
        df_summary: Dictionary with summary statistics
        
    Returns:
        BytesIO object containing the Excel file
    """
    output = BytesIO()
    
    # Clean DataFrames before export - replace NaN/Inf with empty strings
    df_all_clean = df_all.fillna("")
    df_discrepancies_clean = df_discrepancies.fillna("") if not df_discrepancies.empty else df_discrepancies
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#1e40af',
            'font_color': 'white',
            'border': 1
        })
        
        correct_format = workbook.add_format({
            'bg_color': '#d1fae5',  # Light green
            'border': 1
        })
        
        discrepancy_format = workbook.add_format({
            'bg_color': '#fef3c7',  # Light amber
            'border': 1
        })
        
        missing_format = workbook.add_format({
            'bg_color': '#fee2e2',  # Light red
            'border': 1
        })
        
        # Write Summary sheet
        summary_df = pd.DataFrame([df_summary])
        summary_df.to_excel(
            writer,
            sheet_name=EXCEL_SHEET_NAMES['summary'],
            index=False
        )
        
        summary_sheet = writer.sheets[EXCEL_SHEET_NAMES['summary']]
        for col_num, value in enumerate(summary_df.columns.values):
            summary_sheet.write(0, col_num, value, header_format)
        
        # Auto-adjust column widths
        for i, col in enumerate(summary_df.columns):
            max_len = max(
                summary_df[col].astype(str).apply(len).max(),
                len(str(col))
            ) + 2
            summary_sheet.set_column(i, i, max_len)
        
        # Write Discrepancies sheet
        if not df_discrepancies_clean.empty:
            df_discrepancies_clean.to_excel(
                writer,
                sheet_name=EXCEL_SHEET_NAMES['discrepancies'],
                index=False
            )
            
            disc_sheet = writer.sheets[EXCEL_SHEET_NAMES['discrepancies']]
            
            # Apply header format
            for col_num, value in enumerate(df_discrepancies_clean.columns.values):
                disc_sheet.write(0, col_num, value, header_format)
            
            # Apply conditional formatting based on status
            if 'Status' in df_discrepancies_clean.columns:
                status_col_idx = df_discrepancies_clean.columns.get_loc('Status')
                
                for row_num in range(1, len(df_discrepancies_clean) + 1):
                    status = df_discrepancies_clean.iloc[row_num - 1]['Status']
                    
                    if 'Correcto' in str(status):
                        cell_format = correct_format
                    elif 'Discrepancia' in str(status):
                        cell_format = discrepancy_format
                    else:
                        cell_format = missing_format
                    
                    for col_num in range(len(df_discrepancies_clean.columns)):
                        cell_value = sanitize_cell_value(df_discrepancies_clean.iloc[row_num - 1, col_num])
                        disc_sheet.write(
                            row_num, col_num,
                            cell_value,
                            cell_format
                        )
            
            # Auto-adjust column widths
            for i, col in enumerate(df_discrepancies_clean.columns):
                max_len = max(
                    df_discrepancies_clean[col].astype(str).apply(len).max(),
                    len(str(col))
                ) + 2
                disc_sheet.set_column(i, i, min(max_len, 50))
        
        # Write All Data sheet
        df_all_clean.to_excel(
            writer,
            sheet_name=EXCEL_SHEET_NAMES['all_data'],
            index=False
        )
        
        all_sheet = writer.sheets[EXCEL_SHEET_NAMES['all_data']]
        
        # Apply header format
        for col_num, value in enumerate(df_all_clean.columns.values):
            all_sheet.write(0, col_num, value, header_format)
        
        # Auto-adjust column widths
        for i, col in enumerate(df_all_clean.columns):
            max_len = max(
                df_all_clean[col].astype(str).apply(len).max(),
                len(str(col))
            ) + 2
            all_sheet.set_column(i, i, min(max_len, 50))
    
    output.seek(0)
    return output
