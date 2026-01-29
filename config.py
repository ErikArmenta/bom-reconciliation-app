"""
BOM Reconciliation Application - Configuration
Author: Master Engineer Erik Armenta
"""

# Column mapping patterns and aliases
COLUMN_PATTERNS = {
    'part_number': [
        'material no.', 'material no', 'material_no',
        'part number', 'part_number', 'partnumber',
        'sku', 'item code', 'item_code', 'itemcode',
        'material', 'parte', 'código', 'codigo',
        'mat no', 'mat_no', 'matno'
    ],
    'quantity': [
        'quantity', 'qty', 'amount', 'cantidad',
        'cant', 'qnty', 'quant'
    ],
    'unit': [
        'unit', 'uom', 'unit of measure', 'unit_of_measure',
        'unidad', 'um', 'medida', 'units'
    ],
    'description': [
        'description', 'desc', 'material description',
        'item description', 'descripción', 'descripcion',
        'material_description', 'item_description',
        'name', 'nombre', 'text'
    ]
}

# Similarity threshold for fuzzy matching (0.0 to 1.0)
SIMILARITY_THRESHOLD = 0.7

# High similarity threshold for precise matching
HIGH_SIMILARITY_THRESHOLD = 0.85

# Supported file formats
SUPPORTED_FORMATS = ['.xlsx', '.xls', '.csv']

# Maximum rows to display without filtering
MAX_ROWS_WITHOUT_FILTER = 500

# UI Styling
COLORS = {
    'correct': '#10b981',      # Emerald green
    'discrepancy': '#f59e0b',  # Amber
    'missing': '#dc2626',      # Industrial red
    'primary': '#1e40af',      # Blue
    'secondary': '#64748b'     # Slate gray
}

# Status indicators
STATUS_ICONS = {
    'correct': '✅',
    'discrepancy': '⚠️',
    'missing_sap': '❌',
    'missing_software_b': '❌'
}

STATUS_LABELS = {
    'correct': 'Correcto',
    'discrepancy': 'Discrepancia',
    'missing_sap': 'Faltante en SAP',
    'missing_software_b': 'Faltante en Software B'
}

# Export settings
EXCEL_SHEET_NAMES = {
    'summary': 'Resumen',
    'discrepancies': 'Discrepancias',
    'corrected': 'Datos Corregidos',
    'all_data': 'Todos los Datos'
}

# Company information
COMPANY_SLOGAN = "Accuracy is our signature and innovation is our nature"
ENGINEER_SIGNATURE = "Master Engineer Erik Armenta"
LOGO_PATH = "assets/EA_2.png"

# Quantity comparison tolerance (percentage)
QUANTITY_TOLERANCE = 0.01  # 1% tolerance for floating point comparisons
