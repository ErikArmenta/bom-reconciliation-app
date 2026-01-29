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
        # Only include items with issues (discrepancies or missing)
        df_validation = df_comparison[
            df_comparison['Status'].str.contains('Discrepancia|Faltante', na=False)
        ].copy()
    
    # Sort by Part Number for easier floor validation
    df_validation = df_validation.sort_values('Part Number')
    
    # Create validation columns
    df_validation['Validado en Piso'] = '☐'  # Checkbox
    df_validation['Cantidad Real'] = ''
    df_validation['Observaciones'] = ''
    df_validation['Validado Por'] = ''
    df_validation['Fecha'] = ''
    
    # Reorder columns for floor validation
    validation_columns = [
        'Validado en Piso',
        'Part Number',
        'SAP Quantity',
        'Software B Quantity',
        'Cantidad Real',
        'SAP Unit',
        'Software B Unit',
        'SAP Description',
        'Status',
        'Issues',
        'Observaciones',
        'Validado Por',
        'Fecha'
    ]
    
    # Only include columns that exist
    validation_columns = [col for col in validation_columns if col in df_validation.columns]
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
        
        issue_format = workbook.add_format({
            'border': 1,
            'bg_color': '#fee2e2',
            'valign': 'vcenter',
            'text_wrap': True
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
        worksheet.merge_range('A1:M1', 'CHECKLIST DE VALIDACIÓN EN PISO - BOM', title_format)
        
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
                if col_name == 'Validado en Piso':
                    worksheet.write(row_num, col_num, value, checkbox_format)
                elif col_name in ['Cantidad Real', 'Observaciones', 'Validado Por', 'Fecha']:
                    worksheet.write(row_num, col_num, value, input_format)
                elif col_name in ['Status', 'Issues']:
                    worksheet.write(row_num, col_num, str(value) if pd.notna(value) else '', issue_format)
                else:
                    worksheet.write(row_num, col_num, str(value) if pd.notna(value) else '', cell_format)
        
        # Set column widths
        column_widths = {
            'Validado en Piso': 8,
            'Part Number': 15,
            'SAP Quantity': 12,
            'Software B Quantity': 12,
            'Cantidad Real': 12,
            'SAP Unit': 8,
            'Software B Unit': 8,
            'SAP Description': 30,
            'Status': 18,
            'Issues': 25,
            'Observaciones': 25,
            'Validado Por': 15,
            'Fecha': 12
        }
        
        for col_num, col_name in enumerate(df_validation.columns):
            width = column_widths.get(col_name, 15)
            worksheet.set_column(col_num, col_num, width)
        
        # Set row heights
        worksheet.set_row(0, 25)  # Title row
        worksheet.set_row(start_row, 30)  # Header row
        
        # Add instructions sheet
        instructions_sheet = workbook.add_worksheet('Instrucciones')
        instructions_sheet.set_column('A:A', 80)
        
        instructions = [
            ('INSTRUCCIONES PARA VALIDACIÓN EN PISO', title_format),
            ('', None),
            ('1. PREPARACIÓN:', info_format),
            ('   - Imprima este documento', None),
            ('   - Lleve una pluma o marcador', None),
            ('   - Tenga acceso al área de almacén/producción', None),
            ('', None),
            ('2. VALIDACIÓN:', info_format),
            ('   - Localice físicamente cada material por su Part Number', None),
            ('   - Verifique la cantidad real en piso', None),
            ('   - Anote la cantidad real en la columna "Cantidad Real"', None),
            ('   - Marque la casilla ☐ cuando valide el item', None),
            ('', None),
            ('3. OBSERVACIONES:', info_format),
            ('   - Anote cualquier discrepancia encontrada', None),
            ('   - Indique si el material está dañado, vencido, etc.', None),
            ('   - Registre ubicación física si es relevante', None),
            ('', None),
            ('4. FINALIZACIÓN:', info_format),
            ('   - Firme en "Validado Por" cada item verificado', None),
            ('   - Anote la fecha de validación', None),
            ('   - Escanee o fotografíe el documento completado', None),
            ('   - Entregue a ingeniería para actualización del sistema', None),
            ('', None),
            ('IMPORTANTE:', info_format),
            ('⚠️ Solo se incluyen items con DISCREPANCIAS o FALTANTES', None),
            ('⚠️ Priorice items críticos para producción', None),
            ('⚠️ Reporte inmediatamente faltantes críticos', None),
        ]
        
        for row_num, (text, fmt) in enumerate(instructions):
            if fmt:
                instructions_sheet.write(row_num, 0, text, fmt)
            else:
                instructions_sheet.write(row_num, 0, text)
    
    output.seek(0)
    return output
