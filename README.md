# BOM Reconciliation System 🔍

Sistema profesional de reconciliación de Bill of Materials (BOM) entre SAP y software secundario.

**Desarrollado por: Master Engineer Erik Armenta**

## 🎯 Características Principales

### Mapeo Inteligente de Columnas
- Detección automática de columnas similares usando fuzzy matching
- Soporta múltiples variaciones de nombres (Material No., Part Number, SKU, etc.)
- Compatibilidad con nombres en español e inglés
- Scores de confianza para cada mapeo

### Preservación de Datos SAP
- **Crítico**: Preserva ceros a la izquierda (padding) en números de material SAP
- Pre-inspección de archivos para detectar columnas de identificadores
- Uso de `dtype=str` y `converters` para mantener formato original

### Comparación Avanzada
- Validación de cantidades con tolerancia configurable
- Normalización y comparación de unidades de medida
- Comparación de descripciones con fuzzy matching
- Clasificación automática en: Correctos, Discrepancias, Faltantes

### Editor Interactivo
- Edición en tiempo real con `st.data_editor`
- Filtrado inteligente para datasets grandes (>500 filas)
- Opciones de filtro: Ver Todo, Solo Discrepancias, Solo Faltantes
- Cambios reflejados inmediatamente en el reporte

### Visualizaciones Profesionales
- Dashboard de KPIs con métricas clave
- Gráfico de dona "BOM Health Score" con Plotly
- Paleta de colores profesional (Verde esmeralda, Ámbar, Rojo industrial)
- Resumen ejecutivo detallado

### Exportación Avanzada
- Archivos Excel con formato profesional
- Múltiples hojas: Resumen, Discrepancias, Todos los Datos
- Formato condicional basado en estado
- Exportación de CSV para problemas y resumen

## 📦 Instalación

```powershell
# Navegar al directorio del proyecto
cd C:\Users\acer\OneDrive\Escritorio\Dashboard_OEE\ComparadorArchivos

# Instalar dependencias
pip install -r requirements.txt
```

## 🚀 Uso

```powershell
# Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abrirá automáticamente en su navegador en `http://localhost:8501`

## 📋 Flujo de Trabajo

1. **Cargar Archivos**: Suba el BOM de SAP y el BOM de Software B
2. **Revisar Mapeo**: Verifique el mapeo automático de columnas
3. **Ejecutar Comparación**: Haga clic en "Ejecutar Comparación"
4. **Analizar Resultados**: Revise KPIs, gráfico de salud y tabla de datos
5. **Editar Discrepancias**: Corrija valores directamente en la tabla
6. **Descargar Reporte**: Exporte los resultados en Excel o CSV

## 📁 Estructura del Proyecto

```
ComparadorArchivos/
├── app.py                      # Aplicación principal Streamlit
├── config.py                   # Configuración y constantes
├── requirements.txt            # Dependencias Python
├── assets/
│   └── EA_2.png               # Logo de la empresa
├── modules/
│   ├── __init__.py
│   ├── data_handler.py        # Carga y exportación de datos
│   ├── column_mapper.py       # Mapeo inteligente de columnas
│   ├── bom_comparator.py      # Lógica de comparación
│   └── ui_components.py       # Componentes de UI reutilizables
└── test_*.xlsx                # Archivos de prueba (opcional)
```

## 🧪 Archivos de Prueba

El proyecto incluye archivos de prueba que demuestran:
- Preservación de ceros a la izquierda (00123, 00456)
- Materiales correctos (coincidencia exacta)
- Discrepancias en cantidad (20 vs 25)
- Discrepancias en descripción
- Materiales faltantes en SAP
- Materiales faltantes en Software B

## ⚙️ Configuración

Puede ajustar la configuración en `config.py`:

- `SIMILARITY_THRESHOLD`: Umbral de similitud para mapeo (default: 0.7)
- `QUANTITY_TOLERANCE`: Tolerancia para comparación de cantidades (default: 0.01)
- `MAX_ROWS_WITHOUT_FILTER`: Filas máximas antes de activar filtros (default: 500)
- `COLORS`: Paleta de colores para visualizaciones

## 🎨 Características de UI

- **Header**: Logo y eslogan de la empresa
- **Sidebar**: Logo, instrucciones y filtros
- **KPIs**: Métricas en columnas con deltas
- **Health Chart**: Gráfico de dona interactivo con Plotly
- **Data Editor**: Tabla editable con configuración de columnas
- **Footer**: Firma del desarrollador

## 🔧 Tecnologías

- **Streamlit**: Framework de aplicación web
- **Pandas**: Procesamiento de datos
- **Plotly**: Visualizaciones interactivas
- **OpenPyXL**: Lectura de archivos Excel
- **XlsxWriter**: Escritura de archivos Excel con formato
- **difflib**: Fuzzy matching para mapeo de columnas

## 📝 Notas Importantes

### Preservación de Padding SAP
La aplicación implementa lógica crítica para preservar ceros a la izquierda en números de material SAP. Esto previene errores de comparación causados por conversión automática a números.

### Rendimiento con Datasets Grandes
Para BOMs con más de 500 filas, use los filtros en el sidebar para mejorar el rendimiento del editor de datos.

### Mapeo de Columnas
El sistema detecta automáticamente variaciones comunes de nombres de columnas. Si el mapeo no es correcto, verifique que los nombres de columnas sigan convenciones estándar.

## 📄 Licencia

© 2026 Master Engineer Erik Armenta - BOM Reconciliation System

---

**"Accuracy is our signature and innovation is our nature"**
