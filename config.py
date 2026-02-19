"""
BOM Reconciliation Application - Configuration
Author: Master Engineer Erik Armenta
"""

# Column mapping patterns and aliases
# Strict column mapping patterns for SAP
SAP_COLUMN_PATTERNS = {
    'part_number': ['Component number'],
    'quantity': ['Component quantity'],
    'unit': ['Component UoM'],
    'description': ['Description', 'Material Description', 'Item Description'] # Keep generic for description as user didn't specify
}

# Strict column mapping patterns for HPLM
HPLM_COLUMN_PATTERNS = {
    'part_number': ['ERP Part Number'],
    'quantity': ['Quantity'],
    'unit': ['Unit Of Measure'],
    'description': ['Description', 'Material Description'] # Keep generic for description
}

# Generic patterns as fallback (optional, but keeping for safety if strictly needed)
COLUMN_PATTERNS = {
    'part_number': ['Component number', 'ERP Part Number', 'material no.', 'part number'],
    'quantity': ['Component quantity', 'Quantity', 'qty'],
    'unit': ['Component UoM', 'Unit Of Measure', 'unit'],
    'description': ['Description', 'description']
}

# Similarity threshold for fuzzy matching (0.0 to 1.0)
SIMILARITY_THRESHOLD = 0.8 # Increased for stricter matching

# High similarity threshold for precise matching
HIGH_SIMILARITY_THRESHOLD = 0.9

# Supported file formats
SUPPORTED_FORMATS = ['.xlsx', '.xls', '.csv']

# Maximum rows to display without filtering
MAX_ROWS_WITHOUT_FILTER = 500

# UI Styling
COLORS = {
    'correct': '#10b981',      # Emerald green
    'sobra': '#f59e0b',        # Amber (Warning/Surplus)
    'falta': '#dc2626',        # Red (Missing/Deficit)
    'primary': '#1e40af',      # Blue
    'secondary': '#64748b'     # Slate gray
}

# Status indicators
STATUS_ICONS = {
    'correct': '✅',
    'sobra': '⚠️',
    'falta': '❌',
}

STATUS_LABELS = {
    'correct': 'Correcto',
    'sobra': 'Sobra',
    'falta': 'Falta',
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
