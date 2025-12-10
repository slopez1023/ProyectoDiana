# 🚀 Guía de Despliegue - Streamlit Community Cloud (GRATUITO)

## Requisitos Previos
- ✅ Cuenta de GitHub (gratuita)
- ✅ Cuenta de Streamlit Cloud (gratuita)
- ✅ Tu proyecto funcionando localmente

---

## 📋 PASO 1: Preparar el Proyecto

### 1.1 Verificar estructura de archivos
Asegúrate de tener estos archivos en tu carpeta raíz:
```
TableroIndicadores/
├── src/
│   ├── dashboard.py
│   ├── data_processing/
│   ├── analysis/
│   ├── visualization/
│   └── reporting/
├── RE-SM-01 Tablero de Control de Indicadores 2025.xls
├── 63721_bateria-indicadores-sectoriales.xlsx
├── requirements.txt
├── .gitignore
└── README.md
```

### 1.2 Verificar requirements.txt
Ya lo tienes listo ✅

---

## 📦 PASO 2: Subir a GitHub

### 2.1 Crear cuenta en GitHub (si no tienes)
1. Ve a https://github.com
2. Click en "Sign up"
3. Completa el registro (es GRATIS)

### 2.2 Instalar Git (si no lo tienes)
**Windows:**
1. Descarga de: https://git-scm.com/download/win
2. Instala con opciones por defecto

### 2.3 Inicializar repositorio Git
Abre PowerShell en tu carpeta del proyecto y ejecuta:

```powershell
# Configurar Git (primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tuemail@example.com"

# Inicializar repositorio
git init

# Agregar archivos
git add .

# Hacer commit inicial
git commit -m "Initial commit - Tablero de Indicadores MIPG"
```

### 2.4 Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre del repositorio: `tablero-indicadores-mipg`
3. Descripción: "Sistema de análisis de indicadores MIPG"
4. Selecciona "Public" (necesario para Streamlit gratis)
5. ❌ NO marques "Initialize with README" (ya lo tienes)
6. Click en "Create repository"

### 2.5 Subir código a GitHub
GitHub te mostrará comandos, cópialos o usa estos:

```powershell
# Conectar con tu repositorio (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/tablero-indicadores-mipg.git

# Subir archivos
git branch -M main
git push -u origin main
```

**⚠️ IMPORTANTE:** Si es la primera vez, GitHub te pedirá autenticación:
- Usa tu usuario de GitHub
- Como contraseña usa un "Personal Access Token" (te explico abajo cómo crearlo)

### 2.6 Crear Personal Access Token (si te lo pide)
1. Ve a https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Nombre: "Streamlit Deploy"
4. Marcar: `repo` (acceso completo a repositorios)
5. Click "Generate token"
6. **COPIA EL TOKEN** (solo se muestra una vez)
7. Úsalo como contraseña al hacer push

---

## ☁️ PASO 3: Desplegar en Streamlit Cloud

### 3.1 Crear cuenta en Streamlit Cloud
1. Ve a https://share.streamlit.io/
2. Click en "Sign up"
3. **Usa "Continue with GitHub"** (más fácil)
4. Autoriza el acceso

### 3.2 Crear nueva aplicación
1. Click en "New app"
2. Selecciona:
   - **Repository:** `tu-usuario/tablero-indicadores-mipg`
   - **Branch:** `main`
   - **Main file path:** `src/dashboard.py`
3. Click "Deploy!"

### 3.3 Esperar el despliegue
- Primera vez tarda 3-5 minutos
- Verás logs en tiempo real
- Cuando termine, te dará una URL pública

---

## 🎉 PASO 4: Acceder a tu Aplicación

Tu app estará disponible en:
```
https://tu-usuario-tablero-indicadores-mipg.streamlit.app
```

Puedes compartir esta URL con quien quieras ✅

---

## 🔧 PASO 5: Actualizar la Aplicación

Cuando hagas cambios en tu código:

```powershell
# Ver cambios
git status

# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Subir a GitHub
git push
```

**Streamlit Cloud actualizará automáticamente** tu aplicación en 2-3 minutos.

---

## 📊 Límites del Plan Gratuito

✅ **Lo que SÍ incluye (GRATIS):**
- 1 aplicación privada
- Aplicaciones públicas ilimitadas
- 1 GB de almacenamiento
- 1 GB de RAM por app
- Dominio personalizado (tu-app.streamlit.app)
- Actualizaciones automáticas desde GitHub
- HTTPS incluido

❌ **Limitaciones:**
- La app "duerme" después de 7 días sin uso (se reactiva al visitarla)
- Máximo 1 GB de RAM (suficiente para tus Excel)
- No puedes usar bases de datos muy grandes

---

## 🆘 Solución de Problemas Comunes

### Error: "Module not found"
- Asegúrate que el módulo esté en `requirements.txt`
- Verifica la versión de Python (usa 3.9-3.11)

### Error: "File not found" (Excel)
- Los archivos Excel deben estar en la raíz del proyecto
- Verifica que se subieron a GitHub (revisa en github.com)

### App muy lenta
- Los archivos Excel son grandes, primera carga es lenta
- Considera usar caché con `@st.cache_data`

### Error de autenticación Git
- Usa Personal Access Token en lugar de contraseña
- Verifica que el token tenga permisos de `repo`

---

## 💡 Alternativas Gratuitas

Si Streamlit Cloud no te funciona:

1. **Render.com**
   - Plan gratuito: 750 horas/mes
   - Más RAM que Streamlit
   - Configuración más compleja

2. **Railway.app**
   - $5 crédito gratis al mes
   - 500 horas gratis
   - Fácil configuración

3. **Hugging Face Spaces**
   - Totalmente gratuito
   - Perfecto para Streamlit
   - Menos conocido pero muy bueno

---

## 📞 Recursos Útiles

- **Documentación Streamlit Cloud:** https://docs.streamlit.io/streamlit-community-cloud
- **Foro de Streamlit:** https://discuss.streamlit.io/
- **Git Tutorial:** https://git-scm.com/book/es/v2

---

## ✅ Checklist Final

Antes de desplegar, verifica:
- [ ] `requirements.txt` existe y tiene todas las dependencias
- [ ] `.gitignore` existe (para no subir archivos innecesarios)
- [ ] `README.md` existe (opcional pero recomendado)
- [ ] Archivos Excel están en la raíz del proyecto
- [ ] La app funciona localmente con `streamlit run src/dashboard.py`
- [ ] Cuenta de GitHub creada
- [ ] Cuenta de Streamlit Cloud creada
- [ ] Código subido a GitHub
- [ ] App desplegada en Streamlit Cloud

---

## 🎓 Próximos Pasos Recomendados

1. **Configurar dominio personalizado** (opcional)
2. **Agregar autenticación** si necesitas privacidad
3. **Optimizar caché** para mejorar velocidad
4. **Agregar analytics** para ver cuántos usan tu app

---

¡LISTO! Tu aplicación ahora está disponible 24/7 en internet de forma GRATUITA 🎉
