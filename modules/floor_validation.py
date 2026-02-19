"""
Floor Validation Module - BOM Reconciliation Application
Generates floor validation checklists
Author: Master Engineer Erik Armenta
"""

import pandas as pd
import numpy as np
from io import BytesIO
import xlsxwriter
from datetime import datetime

from config import COLORS


def generate_floor_validation_checklist(
    df_comparison: pd.DataFrame,
    include_correct: bool = False
) -> BytesIO:
    """
    Generate a floor validation checklist Excel file optimized for printing.
    
    Args:
        df_comparison: Comparison results DataFrame
        include_correct: Whether to include correct items (default: False, only issues)
        
    Returns:
        BytesIO object containing the Excel file
    """
    output = BytesIO()
    
    # Filter data based on user preference
    if include_correct:
        df_validation = df_comparison.copy()
    else:
        # Only include items with issues (Falta or Sobra)
        df_validation = df_comparison[
            df_comparison['Status'].str.contains('Falta|Sobra', na=False)
        ].copy()
    
    # Sort by Part Number for easier floor validation
    df_validation = df_validation.sort_values('Part Number')
    
    # Create validation columns
    df_validation['Validado'] = '☐'  # Checkbox
    df_validation['Conteo Físico'] = '' # Input for physical count
    
    # Select description (prioritize SAP, then HPLM)
    df_validation['Descripción'] = df_validation.apply(
        lambda x: x['SAP Description'] if pd.notna(x['SAP Description']) and str(x['SAP Description']).strip() != '' 
        else x['HPLM Description'], axis=1
    )
    
    # Reorder columns for floor validation
    # Clean data only: Part, Desc, Qty, Unit
    validation_columns = [
        'Validado',
        'Part Number',
        'Descripción',
        'SAP Quantity',
        'HPLM Quantity',
        'SAP Unit', # Assuming SAP unit is master or they match enough
        'Conteo Físico'
    ]
    
    # Only include all columns (we constructed Description so it exists)
    # Ensure existing cols are present
    final_cols = []
    for col in validation_columns:
        if col in df_validation.columns:
            final_cols.append(col)
        elif col == 'SAP Unit' and 'SAP Unit' in df_validation.columns:
             final_cols.append(col)
        # We need to make sure we don't fail if a column is missing, but our construction ensures they should be there
    
    df_validation = df_validation[validation_columns]
    
    # Create Excel with formatting
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Define formats for printing
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#1e40af',
            'font_color': 'white'
        })
        
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'align': 'center',
            'bg_color': '#3b82f6',
            'font_color': 'white',
            'border': 1,
            'font_size': 10
        })
        
        cell_format = workbook.add_format({
            'border': 1,
            'valign': 'vcenter',
            'text_wrap': True
        })
        
        checkbox_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 14
        })
        
        input_format = workbook.add_format({
            'border': 1,
            'bg_color': '#f0f9ff',
            'valign': 'vcenter'
        })
        
        # Write to worksheet
        worksheet = workbook.add_worksheet('Validación en Piso')
        
        # Set page setup for printing
        worksheet.set_landscape()
        worksheet.set_paper(9)  # A4
        worksheet.fit_to_pages(1, 0)  # Fit to 1 page wide
        worksheet.set_margins(0.5, 0.5, 0.75, 0.75)
        
        # Add title and metadata
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        worksheet.merge_range('A1:G1', 'CHECKLIST DE VALIDACIÓN EN PISO - BOM (SAP vs HPLM)', title_format)
        
        info_format = workbook.add_format({'bold': True, 'font_size': 10})
        worksheet.write('A2', f'Fecha de Generación: {current_date}', info_format)
        worksheet.write('A3', f'Total de Items a Validar: {len(df_validation)}', info_format)
        
        # Write headers (starting at row 4, 0-indexed row 3)
        start_row = 4
        for col_num, column_name in enumerate(df_validation.columns):
            worksheet.write(start_row, col_num, column_name, header_format)
        
        # Write data
        for row_num, row_data in enumerate(df_validation.itertuples(index=False), start=start_row + 1):
            for col_num, value in enumerate(row_data):
                col_name = df_validation.columns[col_num]
                
                # Apply special formatting
                if col_name == 'Validado':
                    worksheet.write(row_num, col_num, value, checkbox_format)
                elif col_name == 'Conteo Físico':
                    worksheet.write(row_num, col_num, value, input_format)
                else:
                    worksheet.write(row_num, col_num, str(value) if pd.notna(value) else '', cell_format)
        
        # Set column widths
        column_widths = {
            'Validado': 8,
            'Part Number': 18,
            'Descripción': 45,
            'SAP Quantity': 12,
            'HPLM Quantity': 12,
            'SAP Unit': 10,
            'Conteo Físico': 15
        }
        
        for col_num, col_name in enumerate(df_validation.columns):
            width = column_widths.get(col_name, 15)
            worksheet.set_column(col_num, col_num, width)
        
        # Set row heights
        worksheet.set_row(0, 25)  # Title row
        worksheet.set_row(start_row, 30)  # Header row
        
        # Add signature block at the bottom
        last_row = start_row + len(df_validation) + 4
        
        signature_format = workbook.add_format({'top': 1, 'align': 'center'})
        
        worksheet.write(last_row, 1, "Realizado Por", signature_format)
        worksheet.write(last_row, 4, "Revisado Por", signature_format)
        worksheet.write(last_row, 6, "Fecha", signature_format)

        # Add instructions sheet (simplified)
        instructions_sheet = workbook.add_worksheet('Instrucciones')
        instructions_sheet.set_column('A:A', 80)
        
        instructions = [
            ('INSTRUCCIONES', title_format),
            ('', None),
            ('1. Verifique físicamente cada número de parte listado.', None),
            ('2. Anote la cantidad real encontrada en la columna "Conteo Físico".', None),
            ('3. Marque la casilla "Validado" una vez verificado.', None),
            ('4. Firme al finalizar.', None)
        ]
        
        for row_num, (text, fmt) in enumerate(instructions):
            if fmt:
                instructions_sheet.write(row_num, 0, text, fmt)
            else:
                instructions_sheet.write(row_num, 0, text)
    
    output.seek(0)
    return output
