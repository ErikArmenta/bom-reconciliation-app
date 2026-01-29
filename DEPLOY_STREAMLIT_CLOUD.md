# 🚀 Guía de Despliegue a Streamlit Cloud

## Paso 1: Preparar el Repositorio Git

### 1.1 Inicializar Git (si no lo has hecho)
```powershell
cd C:\Users\acer\OneDrive\Escritorio\Dashboard_OEE\ComparadorArchivos
git init
```

### 1.2 Crear archivo .gitignore
```powershell
# Crear .gitignore para excluir archivos innecesarios
@"
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.xlsx
*.xls
*.csv
.env
.venv
env/
venv/
"@ | Out-File -FilePath .gitignore -Encoding UTF8
```

### 1.3 Agregar archivos al repositorio
```powershell
git add .
git commit -m "Initial commit - BOM Reconciliation App"
```

---

## Paso 2: Subir a GitHub

### 2.1 Crear Repositorio en GitHub
1. Ve a https://github.com
2. Inicia sesión
3. Clic en el botón **"+"** → **"New repository"**
4. Nombre: `bom-reconciliation-app` (o el que prefieras)
5. Descripción: `BOM Reconciliation System - SAP vs Software B`
6. **NO** marques "Initialize with README" (ya tienes archivos)
7. Clic en **"Create repository"**

### 2.2 Conectar y Subir
```powershell
# Reemplaza 'tu-usuario' con tu usuario de GitHub
git remote add origin https://github.com/tu-usuario/bom-reconciliation-app.git
git branch -M main
git push -u origin main
```

**Nota**: GitHub te pedirá autenticación. Usa tu token de acceso personal.

---

## Paso 3: Desplegar en Streamlit Cloud

### 3.1 Crear Cuenta en Streamlit Cloud
1. Ve a https://share.streamlit.io
2. Clic en **"Sign up"** o **"Continue with GitHub"**
3. Autoriza Streamlit Cloud a acceder a tu GitHub

### 3.2 Desplegar la App
1. Clic en **"New app"**
2. Selecciona:
   - **Repository**: `tu-usuario/bom-reconciliation-app`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. **Advanced settings** (opcional):
   - Python version: `3.11` o `3.12`
4. Clic en **"Deploy!"**

### 3.3 Esperar Despliegue
- Streamlit Cloud instalará automáticamente las dependencias de `requirements.txt`
- El proceso toma 2-5 minutos
- Verás logs en tiempo real

---

## 🎯 URL de tu App

Una vez desplegada, tu app estará disponible en:
```
https://tu-usuario-bom-reconciliation-app-xxxxx.streamlit.app
```

Puedes compartir esta URL con tu equipo.

---

## 🔧 Configuración Adicional (Opcional)

### Cambiar Nombre de la App
1. En Streamlit Cloud, ve a tu app
2. Clic en **"Settings"** → **"General"**
3. Cambia el **App URL** a algo más corto

### Configurar Secretos (si necesitas)
Si tu app necesita variables de entorno:
1. **Settings** → **"Secrets"**
2. Agrega en formato TOML:
```toml
# Ejemplo (no necesario para esta app)
[database]
host = "localhost"
```

### Hacer la App Privada
1. **Settings** → **"Sharing"**
2. Selecciona **"Private"**
3. Invita usuarios específicos por email

---

## 🔄 Actualizar la App

Cada vez que hagas cambios:

```powershell
# 1. Hacer cambios en el código
# 2. Guardar archivos
# 3. Commit y push
git add .
git commit -m "Descripción de cambios"
git push
```

**Streamlit Cloud detectará automáticamente los cambios y re-desplegará la app.**

---

## ⚠️ Limitaciones de Streamlit Cloud (Plan Gratuito)

- **1 app privada** o **ilimitadas públicas**
- **1 GB de RAM** por app
- **1 CPU** compartido
- **Sin límite de usuarios** (pero puede ser lento con muchos usuarios simultáneos)

Para apps privadas o más recursos, considera el plan **Team** ($20/mes).

---

## 🐛 Solución de Problemas

### Error: "Module not found"
**Solución**: Verifica que `requirements.txt` esté en la raíz del repo y contenga todas las dependencias.

### Error: "File not found: app.py"
**Solución**: Asegúrate de que `app.py` esté en la raíz del repositorio, no en una subcarpeta.

### La app se reinicia constantemente
**Solución**: Revisa los logs en Streamlit Cloud. Probablemente hay un error en el código.

### Error con el logo EA_2.png
**Solución**: Asegúrate de que la carpeta `assets/` y el archivo `EA_2.png` estén en el repositorio.

---

## 📋 Checklist de Despliegue

Antes de desplegar, verifica:

- [ ] `requirements.txt` existe y está completo
- [ ] `app.py` está en la raíz
- [ ] Carpeta `modules/` con todos los archivos `.py`
- [ ] Carpeta `assets/` con `EA_2.png`
- [ ] `config.py` en la raíz
- [ ] `.gitignore` creado (para excluir archivos temporales)
- [ ] Repositorio en GitHub creado y actualizado
- [ ] Cuenta en Streamlit Cloud creada

---

## 🎓 Comandos Rápidos de Referencia

```powershell
# Inicializar Git
git init

# Ver estado
git status

# Agregar archivos
git add .

# Commit
git commit -m "Mensaje"

# Push a GitHub
git push origin main

# Ver remotes
git remote -v

# Pull cambios
git pull origin main
```

---

## 📞 Recursos Adicionales

- **Documentación Streamlit Cloud**: https://docs.streamlit.io/streamlit-community-cloud
- **GitHub Docs**: https://docs.github.com
- **Streamlit Community**: https://discuss.streamlit.io

---

## ✅ Verificación Post-Despliegue

Después de desplegar, prueba:

1. [ ] La app carga correctamente
2. [ ] El logo se muestra
3. [ ] Puedes subir archivos de prueba
4. [ ] La comparación funciona
5. [ ] Los 4 botones de descarga funcionan
6. [ ] El checklist de piso se genera correctamente

---

**¡Listo! Tu app estará disponible 24/7 en la nube.**

**Desarrollado por**: Master Engineer Erik Armenta

**"Accuracy is our signature and innovation is our nature"**
