# 🚀 Guía Rápida de Uso - BOM Reconciliation System

## Inicio Rápido

### 1. Ejecutar la Aplicación
```powershell
cd C:\Users\acer\OneDrive\Escritorio\Dashboard_OEE\ComparadorArchivos
streamlit run app.py
```

### 2. Cargar Archivos
- **SAP BOM**: Clic en "Cargar archivo SAP" → Seleccionar archivo Excel/CSV
- **Software B BOM**: Clic en "Cargar archivo Software B" → Seleccionar archivo Excel/CSV

### 3. Revisar Mapeo Automático
- Expandir "🔗 Mapeo SAP" para ver confianza de mapeo
- Expandir "🔗 Mapeo Software B" para ver confianza de mapeo
- ✅ = Alta confianza (>85%), ⚠️ = Confianza media (>70%)

### 4. Ejecutar Comparación
- Clic en botón "🚀 Ejecutar Comparación"
- Esperar procesamiento (automático)

### 5. Analizar Resultados

**KPIs Principales:**
- Total Materiales
- ✅ Correctos (coincidencia perfecta)
- ⚠️ Discrepancias (diferencias en datos)
- ❌ Faltantes (en SAP o Software B)

**Gráfico de Salud:**
- Verde: Materiales correctos
- Ámbar: Discrepancias
- Rojo: Faltantes

### 6. Editar Datos (Opcional)
- Hacer clic en cualquier celda de la tabla
- Escribir el valor correcto
- Los cambios se guardan automáticamente

### 7. Filtrar Datos (Para BOMs grandes >500 filas)
En el **Sidebar**, seleccionar:
- **Ver Todo**: Todos los registros
- **Solo Discrepancias**: Solo problemas de datos
- **Solo Faltantes**: Solo materiales faltantes

### 8. Descargar Reportes

**Opciones de descarga:**
1. **📊 Reporte Completo** (Excel): Incluye todas las hojas con formato
2. **⚠️ Solo Problemas** (CSV): Solo discrepancias y faltantes
3. **📈 Resumen** (CSV): Estadísticas resumidas

---

## 📝 Formatos de Archivo Soportados

- Excel: `.xlsx`, `.xls`
- CSV: `.csv`

## 🔑 Columnas Reconocidas Automáticamente

### Part Number (Requerido)
- Material No., Part Number, SKU, Item Code, Parte, Código

### Quantity
- Quantity, Qty, Amount, Cantidad

### Unit
- Unit, UOM, Unit of Measure, Unidad

### Description
- Description, Material Description, Item Description, Descripción

---

## ⚠️ Notas Importantes

### Preservación de Ceros a la Izquierda
✅ La aplicación **preserva automáticamente** los ceros a la izquierda en números de material SAP (ej: `00123` no se convierte en `123`)

### Rendimiento con Datasets Grandes
- Para BOMs >500 filas, use los **filtros en el sidebar**
- Esto mejora significativamente el rendimiento del editor

### Tolerancia de Comparación
- Cantidades: 1% de tolerancia para decimales
- Descripciones: 80% de similitud mínima
- Unidades: Normalización automática (PCS=PC=PIECE)

---

## 🎨 Interpretación de Resultados

| Icono | Status | Significado |
|-------|--------|-------------|
| ✅ | Correcto | Todos los campos coinciden perfectamente |
| ⚠️ | Discrepancia | Uno o más campos no coinciden |
| ❌ | Faltante en SAP | Material existe solo en Software B |
| ❌ | Faltante en Software B | Material existe solo en SAP |

---

## 🔧 Solución de Problemas

### "No se pudo mapear columnas críticas"
**Solución**: Verifique que su archivo tenga una columna de Part Number con nombre similar a: Material No., Part Number, SKU, etc.

### "El archivo está vacío"
**Solución**: Verifique que el archivo Excel/CSV contenga datos y no esté corrupto.

### "Formato no soportado"
**Solución**: Use solo archivos `.xlsx`, `.xls`, o `.csv`

### La aplicación está lenta
**Solución**: Active los filtros en el sidebar (Solo Discrepancias o Solo Faltantes)

---

## 📞 Soporte

**Desarrollado por**: Master Engineer Erik Armenta

**"Accuracy is our signature and innovation is our nature"**
