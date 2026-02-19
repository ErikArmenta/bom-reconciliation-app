"""
BOM Reconciliation Application
Main Streamlit Application
Author: Master Engineer Erik Armenta
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Import custom modules
from modules.data_handler import load_file, validate_dataframe, export_to_excel
from modules.column_mapper import map_bom_columns, validate_mapping
from modules.bom_comparator import compare_boms, generate_status_report
from modules.floor_validation import generate_floor_validation_checklist
from modules.ui_components import (
    render_header, render_sidebar_logo, render_kpi_metrics,
    render_health_chart, render_footer, render_file_uploader,
    render_mapping_info, render_data_filter_options, apply_data_filter
)
from config import MAX_ROWS_WITHOUT_FILTER

# Page configuration
st.set_page_config(
    page_title="BOM Reconciliation System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'comparison_results' not in st.session_state:
    st.session_state.comparison_results = None
if 'status_report' not in st.session_state:
    st.session_state.status_report = None
if 'edited_data' not in st.session_state:
    st.session_state.edited_data = None


def main():
    """Main application function."""
    
    # Render header
    render_header()
    
    # Render sidebar logo
    render_sidebar_logo()
    
    # Sidebar instructions
    st.sidebar.markdown("### 📋 Instrucciones")
    st.sidebar.info(
        "1. Cargue el archivo BOM de SAP\n"
        "2. Cargue el archivo BOM de HPLM\n"
        "3. Revise el mapeo de columnas\n"
        "4. Analice los resultados\n"
        "5. Edite discrepancias si es necesario\n"
        "6. Descargue el reporte reconciliado"
    )
    
    st.sidebar.markdown("---")
    
    # File uploaders
    st.markdown("## 📁 Carga de Archivos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### SAP BOM")
        sap_file = render_file_uploader(
            "Cargar archivo SAP",
            key="sap_uploader",
            help_text="Archivo BOM exportado de SAP (Excel o CSV)"
        )
    
    with col2:
        st.markdown("### HPLM BOM")
        software_b_file = render_file_uploader(
            "Cargar archivo HPLM",
            key="software_b_uploader",
            help_text="Archivo BOM del sistema HPLM (Excel o CSV)"
        )
    
    # Process files if both are uploaded
    if sap_file and software_b_file:
        st.markdown("---")
        
        with st.spinner("🔄 Procesando archivos..."):
            # Load SAP file
            df_sap, error_sap = load_file(sap_file, sap_file.name)
            if error_sap:
                st.error(f"❌ Error en archivo SAP: {error_sap}")
                return
            
            # Load HPLM file
            df_software_b, error_sb = load_file(software_b_file, software_b_file.name)
            if error_sb:
                st.error(f"❌ Error en archivo HPLM: {error_sb}")
                return
            
            # Validate DataFrames
            error_val_sap = validate_dataframe(df_sap, "SAP")
            if error_val_sap:
                st.error(f"❌ {error_val_sap}")
                return
            
            error_val_sb = validate_dataframe(df_software_b, "HPLM")
            if error_val_sb:
                st.error(f"❌ {error_val_sb}")
                return
            
            st.success("✅ Archivos cargados exitosamente")
            
            # Display file info
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📊 SAP: {len(df_sap)} filas, {len(df_sap.columns)} columnas")
            with col2:
                st.info(f"📊 HPLM: {len(df_software_b)} filas, {len(df_software_b.columns)} columnas")
        
        st.markdown("---")
        
        # Column mapping
        st.markdown("## 🔗 Mapeo de Columnas")
        
        with st.spinner("🔍 Mapeando columnas..."):
            mapping_sap = map_bom_columns(df_sap, "SAP")
            mapping_software_b = map_bom_columns(df_software_b, "HPLM")
        
        col1, col2 = st.columns(2)
        
        with col1:
            render_mapping_info(mapping_sap, "Mapeo SAP")
        
        with col2:
            render_mapping_info(mapping_software_b, "Mapeo HPLM")
        
        # Validate mappings
        valid_sap, error_sap = validate_mapping(mapping_sap)
        valid_sb, error_sb = validate_mapping(mapping_software_b)
        
        if not valid_sap:
            st.error(f"❌ Error en mapeo SAP: {error_sap}")
            return
        
        if not valid_sb:
            st.error(f"❌ Error en mapeo HPLM: {error_sb}")
            return
        
        st.success("✅ Mapeo de columnas completado exitosamente")
        
        st.markdown("---")
        
        # Comparison
        st.markdown("## 🔍 Análisis de Reconciliación")
        
        if st.button("🚀 Ejecutar Comparación", type="primary", use_container_width=True):
            with st.spinner("⚙️ Comparando BOMs..."):
                # Perform comparison
                df_comparison = compare_boms(
                    df_sap, df_software_b,
                    mapping_sap, mapping_software_b
                )
                
                # Generate status report
                status_report = generate_status_report(df_comparison)
                
                # Store in session state
                st.session_state.comparison_results = df_comparison
                st.session_state.status_report = status_report
                st.session_state.edited_data = df_comparison.copy()
            
            st.success("✅ Comparación completada")
            st.rerun()
        
        # Display results if available
        if st.session_state.comparison_results is not None:
            st.markdown("---")
            
            # Display KPI metrics
            render_kpi_metrics(st.session_state.status_report)
            
            st.markdown("---")
            
            # Display health chart
            col1, col2 = st.columns([2, 1])
            
            with col1:
                render_health_chart(st.session_state.status_report)
            
            with col2:
                st.markdown("### 📈 Resumen Ejecutivo")
                report = st.session_state.status_report
                
                st.markdown(f"""
                - **Total de Materiales**: {report['Total Materiales']}
                - **Correctos**: {report['Correctos']} ({report['Porcentaje Correcto']}%)
                - **Con Problemas**: {report['Total con Problemas']} ({report['Porcentaje con Problemas']}%)
                
                - Discrepancias: {report.get('Discrepancias', 0)}
                - Faltantes en HPLM: {report.get('Faltantes en Software B', 0)}
                - Sobrantes en HPLM: {report.get('Sobrantes/Excedentes (+)', 0)}
                """)
            
            st.markdown("---")
            
            # Data editor with filtering
            st.markdown("## 📝 Editor de Datos")
            
            df_to_display = st.session_state.edited_data
            total_rows = len(df_to_display)
            
            # Show filter options if dataset is large
            if total_rows > MAX_ROWS_WITHOUT_FILTER:
                st.info(
                    f"ℹ️ Dataset grande detectado ({total_rows} filas). "
                    f"Use el filtro en el sidebar para mejorar el rendimiento."
                )
                filter_option = render_data_filter_options()
                df_filtered = apply_data_filter(df_to_display, filter_option)
                
                st.markdown(f"**Mostrando**: {len(df_filtered)} de {total_rows} filas")
            else:
                df_filtered = df_to_display
                st.markdown(f"**Total de filas**: {total_rows}")
            
            # Data editor
            st.markdown("""
                <div style='background-color: #f0f9ff; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;'>
                    <p style='margin: 0; color: #1e40af;'>
                        💡 <strong>Tip:</strong> Puede editar los valores directamente en la tabla. 
                        Los cambios se reflejarán en tiempo real en el archivo de descarga.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            edited_df = st.data_editor(
                df_filtered,
                use_container_width=True,
                num_rows="fixed",
                hide_index=True,
                column_config={
                    "Status": st.column_config.TextColumn(
                        "Status",
                        help="Estado de la reconciliación",
                        width="medium"
                    ),
                    "Part Number": st.column_config.TextColumn(
                        "Part Number",
                        help="Número de parte / Material",
                        width="medium"
                    ),
                    "Issues": st.column_config.TextColumn(
                        "Issues",
                        help="Descripción de problemas encontrados",
                        width="large"
                    )
                }
            )
            
            # Update session state with edited data
            if not edited_df.equals(df_filtered):
                # Update the edited data in session state
                st.session_state.edited_data.update(edited_df)
                st.success("✅ Cambios guardados en memoria")
            
            st.markdown("---")
            
            # Download section
            st.markdown("## 📥 Descargar Resultados")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Export all data
                excel_buffer = export_to_excel(
                    st.session_state.edited_data,
                    st.session_state.edited_data[
                        st.session_state.edited_data['Status'].str.contains('Falta|Sobra', na=False)
                    ],
                    st.session_state.status_report
                )
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"BOM_Reconciliation_{timestamp}.xlsx"
                
                st.download_button(
                    label="📊 Reporte Completo",
                    data=excel_buffer,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    help="Reporte completo con todas las hojas y formato"
                )
            
            with col2:
                # Floor validation checklist
                floor_checklist = generate_floor_validation_checklist(
                    st.session_state.edited_data,
                    include_correct=False
                )
                
                st.download_button(
                    label="📋 Checklist de Piso",
                    data=floor_checklist,
                    file_name=f"Checklist_Validacion_Piso_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    help="Checklist optimizado para validación física en piso"
                )
            
            with col3:
                # Export only discrepancies
                # Filter by simple "Falta" or "Sobra" presence in Status
                df_issues = st.session_state.edited_data[
                    st.session_state.edited_data['Status'].str.contains('Falta|Sobra', na=False)
                ]
                
                if not df_issues.empty:
                    csv_issues = df_issues.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⚠️ Solo Problemas",
                        data=csv_issues,
                        file_name=f"BOM_Issues_{timestamp}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        help="Solo discrepancias y faltantes en CSV"
                    )
                else:
                    st.info("Sin problemas")
            
            with col4:
                # Export summary
                summary_df = pd.DataFrame([st.session_state.status_report])
                csv_summary = summary_df.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📈 Resumen",
                    data=csv_summary,
                    file_name=f"BOM_Summary_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    help="Estadísticas resumidas en CSV"
                )
    
    else:
        # Show placeholder when no files uploaded
        st.info("👆 Por favor, cargue ambos archivos BOM para comenzar la reconciliación")
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()
