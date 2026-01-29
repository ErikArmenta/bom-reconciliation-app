# 📋 Checklist de Validación en Piso - Guía de Uso

## ¿Qué es el Checklist de Validación en Piso?

Es un archivo Excel **optimizado para impresión** que te permite validar físicamente los materiales en el almacén o piso de producción. Incluye:

✅ **Casillas de verificación** (☐) para marcar items validados  
✅ **Espacio para cantidad real** encontrada en piso  
✅ **Columna de observaciones** para notas  
✅ **Campos de firma y fecha** para trazabilidad  
✅ **Formato de impresión** optimizado (landscape A4)  
✅ **Hoja de instrucciones** incluida  

---

## 🎯 ¿Cuándo Usar Este Checklist?

- Cuando necesitas **validar físicamente** las discrepancias encontradas
- Para **auditorías de inventario** basadas en el análisis BOM
- Cuando hay **diferencias significativas** entre SAP y Software B
- Para **verificar materiales faltantes** reportados por el sistema

---

## 📥 Cómo Generar el Checklist

1. **Ejecuta la comparación** de BOMs en la aplicación
2. Ve a la sección **"📥 Descargar Resultados"**
3. Haz clic en **"📋 Checklist de Piso"**
4. El archivo se descargará automáticamente

**Nota**: El checklist **solo incluye items con problemas** (discrepancias y faltantes). Los materiales correctos NO se incluyen para optimizar el trabajo en piso.

---

## 📋 Contenido del Checklist

### Hoja 1: Validación en Piso

| Columna | Descripción | Uso |
|---------|-------------|-----|
| **Validado en Piso** | Casilla ☐ | Marca con ✓ cuando valides el item |
| **Part Number** | Número de material | Para localizar el material |
| **SAP Quantity** | Cantidad en SAP | Referencia del sistema |
| **Software B Quantity** | Cantidad en Software B | Referencia del sistema secundario |
| **Cantidad Real** | Campo vacío | **Escribe la cantidad física real** |
| **SAP Unit** / **Software B Unit** | Unidades | Para verificar unidad de medida |
| **SAP Description** | Descripción | Para identificar el material |
| **Status** | Estado | Tipo de problema detectado |
| **Issues** | Problemas | Descripción del problema |
| **Observaciones** | Campo vacío | **Anota cualquier hallazgo** |
| **Validado Por** | Campo vacío | **Firma o iniciales** |
| **Fecha** | Campo vacío | **Fecha de validación** |

### Hoja 2: Instrucciones

Incluye instrucciones paso a paso para el personal de piso.

---

## 🚶 Flujo de Trabajo Recomendado

### 1. **Preparación** (Oficina)
```
✓ Descarga el checklist de piso
✓ Imprime el documento
✓ Prepara pluma/marcador
✓ Revisa los items prioritarios
```

### 2. **Validación** (Piso/Almacén)
```
Para cada material en el checklist:
  1. Localiza el material por Part Number
  2. Cuenta la cantidad física real
  3. Anota la cantidad en "Cantidad Real"
  4. Marca la casilla ☐ → ✓
  5. Anota observaciones si es necesario
  6. Firma en "Validado Por"
  7. Anota la fecha
```

### 3. **Reporte** (Oficina)
```
✓ Escanea o fotografía el checklist completado
✓ Compara cantidades reales vs sistema
✓ Actualiza SAP/Software B según corresponda
✓ Archiva el checklist para trazabilidad
```

---

## 💡 Tips para Validación Efectiva

### Priorización
- ⚡ **Primero**: Materiales críticos para producción
- ⚠️ **Segundo**: Discrepancias grandes (>20% diferencia)
- 📋 **Tercero**: Faltantes reportados
- ✅ **Último**: Discrepancias menores

### Observaciones Útiles
Anota información como:
- 🏷️ Ubicación física exacta (rack, pasillo, nivel)
- 📦 Estado del material (dañado, vencido, etc.)
- 🔄 Movimientos recientes (recién recibido, en tránsito)
- ⚠️ Problemas de etiquetado o identificación
- 📝 Diferencias en unidad de medida

### Casos Especiales

**Material No Encontrado:**
```
Cantidad Real: 0
Observaciones: "No localizado en almacén. Verificar ubicación en SAP."
```

**Material Dañado:**
```
Cantidad Real: [cantidad física]
Observaciones: "5 pzas dañadas, 10 pzas OK. Total físico: 15"
```

**Diferencia en Unidad:**
```
Cantidad Real: [cantidad convertida]
Observaciones: "Sistema: KG, Físico: Gramos. Convertido: X KG"
```

---

## 📊 Formato de Impresión

El checklist está configurado para:
- **Orientación**: Horizontal (Landscape)
- **Tamaño**: A4
- **Ajuste**: 1 página de ancho (altura automática)
- **Márgenes**: 0.5" todos los lados
- **Encabezados**: Se repiten en cada página

---

## ✅ Checklist de Validación Completada

Después de validar en piso, verifica que:

- [ ] Todos los items tienen casilla marcada ✓
- [ ] Todas las "Cantidad Real" están llenas
- [ ] Observaciones anotadas donde sea relevante
- [ ] Firma en cada item validado
- [ ] Fecha de validación anotada
- [ ] Documento escaneado/fotografiado
- [ ] Resultados comunicados a ingeniería
- [ ] Sistemas actualizados según hallazgos

---

## 🔄 Actualización de Sistemas

Basándote en las cantidades reales encontradas:

### Si Cantidad Real = SAP
→ Actualizar Software B

### Si Cantidad Real = Software B
→ Actualizar SAP

### Si Cantidad Real ≠ Ambos
→ Actualizar SAP y Software B con cantidad real  
→ Investigar causa de discrepancia

---

## 📞 Soporte

Para dudas sobre el checklist o el proceso de validación:

**Desarrollado por**: Master Engineer Erik Armenta

---

**"Accuracy is our signature and innovation is our nature"**
