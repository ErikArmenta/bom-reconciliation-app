"""
UI Components Module - BOM Reconciliation Application
Reusable Streamlit UI components
Author: Master Engineer Erik Armenta
"""

import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
from typing import Dict

from config import (
    COMPANY_SLOGAN, ENGINEER_SIGNATURE, LOGO_PATH,
    COLORS, SUPPORTED_FORMATS
)


def render_header():
    """
    Render application header with logo and slogan.
    """
    # Custom CSS for header styling
    st.markdown("""
        <style>
        .main-header {
            text-align: center;
            padding: 1rem 0;
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
        }
        .slogan {
            font-size: 1.2rem;
            font-style: italic;
            color: #e0e7ff;
            margin-top: 0.5rem;
        }
        .app-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="main-header">
            <h1 class="app-title">🔍 BOM Reconciliation System</h1>
            <p class="slogan">"{COMPANY_SLOGAN}"</p>
        </div>
    """, unsafe_allow_html=True)


def render_sidebar_logo():
    """
    Render logo in sidebar.
    """
    logo_path = Path(LOGO_PATH)
    
    if logo_path.exists():
        st.sidebar.image(str(logo_path), use_container_width=True)
    else:
        # Placeholder if logo doesn't exist
        st.sidebar.markdown("""
            <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); border-radius: 10px;'>
                <h1 style='color: white; margin: 0;'>EA</h1>
                <p style='color: #e0e7ff; margin: 0; font-size: 0.8rem;'>Engineering Analytics</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")


def render_kpi_metrics(report: Dict):
    """
    Render KPI metrics in columns.
    
    Args:
        report: Status report dictionary from generate_status_report
    """
    st.markdown("### 📊 Métricas de Reconciliación")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Materiales",
            value=report['Total Materiales'],
            delta=None
        )
    
    with col2:
        st.metric(
            label="✅ Correctos",
            value=report['Correctos'],
            delta=f"{report['Porcentaje Correcto']}%"
        )
    
    with col3:
        st.metric(
            label="⚠️ Sobrantes (SAP)",
            value=report.get('Sobrantes/Excedentes (+)', 0),
            delta=None,
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="❌ Faltantes (SAP)",
            value=report.get('Faltantes/Diferencias (-)', 0),
            delta=None,
            delta_color="inverse"
        )


def render_health_chart(report: Dict):
    """
    Render BOM Health Score donut chart using Plotly.
    
    Args:
        report: Status report dictionary from generate_status_report
    """
    # Prepare data
    labels = ['Correctos', 'Sobrantes', 'Faltantes']
    values = [
        report['Correctos'],
        report.get('Sobrantes/Excedentes (+)', 0),
        report.get('Faltantes/Diferencias (-)', 0)
    ]
    
    # Professional color palette
    colors_list = [COLORS['correct'], COLORS['sobra'], COLORS['falta']]
    
    # Create donut chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(
            colors=colors_list,
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
    )])
    
    # Calculate health score
    total = report['Total Materiales']
    health_score = (report['Correctos'] / total * 100) if total > 0 else 0
    
    # Update layout
    fig.update_layout(
        title={
            'text': f"BOM Health Score: {health_score:.1f}%",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['primary'], 'family': 'Arial Black'}
        },
        annotations=[
            dict(
                text=f'{health_score:.1f}%',
                x=0.5, y=0.5,
                font=dict(size=32, color=COLORS['primary'], family='Arial Black'),
                showarrow=False
            )
        ],
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=400,
        margin=dict(t=80, b=80, l=20, r=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_footer():
    """
    Render footer with engineer signature at page bottom.
    """
    st.markdown("---")
    st.markdown(f"""
        <div style='text-align: center; padding: 1rem; color: {COLORS['secondary']}; font-size: 0.9rem;'>
            <p style='margin: 0;'>Developed by <strong>{ENGINEER_SIGNATURE}</strong></p>
            <p style='margin: 0; font-size: 0.8rem;'>© 2026 - BOM Reconciliation System</p>
        </div>
    """, unsafe_allow_html=True)


def render_file_uploader(label: str, key: str, help_text: str = None):
    """
    Render standardized file uploader component.
    
    Args:
        label: Label for the uploader
        key: Unique key for the uploader
        help_text: Optional help text
        
    Returns:
        Uploaded file object or None
    """
    accepted_formats = SUPPORTED_FORMATS
    
    uploaded_file = st.file_uploader(
        label,
        type=[fmt.replace('.', '') for fmt in accepted_formats],
        key=key,
        help=help_text or f"Formatos soportados: {', '.join(accepted_formats)}"
    )
    
    return uploaded_file


def render_mapping_info(mapping: Dict, title: str):
    """
    Render column mapping information in an expander.
    
    Args:
        mapping: Mapping dictionary from map_bom_columns
        title: Title for the expander
    """
    with st.expander(f"🔗 {title}", expanded=False):
        from modules.column_mapper import get_mapping_summary
        
        st.markdown(get_mapping_summary(mapping))
        
        if mapping['missing_columns']:
            st.warning(f"⚠️ Columnas no mapeadas: {', '.join(mapping['missing_columns'])}")


def render_data_filter_options():
    """
    Render filter options for data editor in sidebar.
    
    Returns:
        Selected filter option
    """
    st.sidebar.markdown("### 🔍 Filtro de Visualización")
    
    filter_option = st.sidebar.radio(
        "Mostrar:",
        options=['Ver Todo', 'Solo Problemas (Falta/Sobra)', 'Solo Sobrantes', 'Solo Faltantes'],
        index=0,
        help="Filtra los datos mostrados en el editor para mejorar el rendimiento con datasets grandes"
    )
    
    return filter_option


def apply_data_filter(df, filter_option: str):
    """
    Apply filter to DataFrame based on user selection.
    
    Args:
        df: DataFrame to filter
        filter_option: Filter option selected by user
        
    Returns:
        Filtered DataFrame
    """
    if filter_option == 'Solo Problemas (Falta/Sobra)':
        return df[df['Status'].str.contains('Falta|Sobra', na=False)]
    elif filter_option == 'Solo Sobrantes':
        return df[df['Status'].str.contains('Sobra', na=False)]
    elif filter_option == 'Solo Faltantes':
        return df[df['Status'].str.contains('Falta', na=False)]
    else:
        return df
