# 🚀 INICIO RÁPIDO - Sistema de Indicadores MIPG

## ⚡ 3 Pasos para Empezar

### 1️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Ejecutar Análisis
```bash
python main.py
```

### 3️⃣ Abrir Dashboard

**IMPORTANTE:** Primero activa el entorno virtual:

**En PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**En CMD:**
```cmd
.venv\Scripts\activate.bat
```

Luego ejecuta el dashboard:
```bash
streamlit run src/dashboard.py
```

> **Nota:** Si aparece error de permisos en PowerShell, ejecuta primero:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## 📋 Requisitos Previos

- ✅ Python 3.8 o superior
- ✅ Archivo Excel en la raíz del proyecto
- ✅ Conexión a internet (solo para instalación)

---

## 🎯 ¿Qué hace cada comando?

### `python main.py`
Ejecuta el proceso completo:
- ✅ Carga el archivo Excel
- ✅ Analiza todos los indicadores
- ✅ Genera gráficos interactivos
- ✅ Crea reporte PDF ejecutivo

**Salida:**
- Gráficos en: `output/charts/`
- Reportes en: `output/reports/`
- Log en: `sistema_indicadores.log`

### `streamlit run src/dashboard.py`
Abre el dashboard interactivo en tu navegador:
- 🔍 Explorar indicadores
- 📊 Ver gráficos en tiempo real
- 🎯 Aplicar filtros
- 📄 Generar reportes personalizados

**URL:** http://localhost:8501

---

## 📁 Estructura de Archivos

```
TableroIndicadores/
│
├── 📄 main.py                    ← Ejecutar este archivo
├── 📄 ejemplos.py               ← Ver ejemplos de código
├── 📄 requirements.txt          ← Dependencias necesarias
├── 📄 README.md                 ← Documentación completa
│
├── 📁 src/                      ← Código fuente
│   ├── dashboard.py             ← Dashboard Streamlit
│   ├── data_processing/         ← Carga de datos
│   ├── analysis/                ← Análisis de indicadores
│   ├── visualization/           ← Generación de gráficos
│   ├── reporting/               ← Informes PDF
│   └── utils/                   ← Utilidades
│
├── 📁 data/                     ← Datos
│   ├── input/                   ← Archivos de entrada
│   └── processed/               ← Datos procesados
│
├── 📁 output/                   ← Resultados
│   ├── charts/                  ← Gráficos generados
│   └── reports/                 ← Reportes PDF
│
├── 📁 docs/                     ← Documentación
│   ├── ARQUITECTURA.md          ← Diseño técnico
│   ├── GUIA_USO.md             ← Manual de usuario
│   └── RESUMEN_EJECUTIVO.md    ← Resumen del proyecto
│
└── 📄 RE-SM-01 Tablero...xls   ← TU ARCHIVO EXCEL AQUÍ
```

---

## 🎓 Siguientes Pasos

### Para Usuarios
1. Lee la [Guía de Uso](docs/GUIA_USO.md)
2. Explora el dashboard
3. Genera tu primer reporte

### Para Desarrolladores
1. Lee la [Arquitectura](docs/ARQUITECTURA.md)
2. Revisa los [ejemplos.py](ejemplos.py)
3. Consulta el código documentado

---

## ⚠️ Solución Rápida de Problemas

### Error: "Archivo no encontrado"
✅ **Solución:** Coloca el archivo Excel en la raíz del proyecto

### Error: "ModuleNotFoundError"
✅ **Solución:** 
```bash
pip install -r requirements.txt
```

### Dashboard no se abre
✅ **Solución:**
```bash
streamlit cache clear
streamlit run src/dashboard.py
```

---

## 📞 Ayuda Adicional

- 📖 Documentación completa: [README.md](README.md)
- 🎓 Manual de usuario: [docs/GUIA_USO.md](docs/GUIA_USO.md)
- 🏗️ Documentación técnica: [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md)
- 📊 Resumen ejecutivo: [docs/RESUMEN_EJECUTIVO.md](docs/RESUMEN_EJECUTIVO.md)

---

## ✅ Checklist de Verificación

Antes de ejecutar, verifica que tengas:

- [ ] Python 3.8+ instalado (`python --version`)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo Excel en la raíz del proyecto
- [ ] Permisos de escritura en carpetas `output/`

---

**¡Listo! Ya puedes usar el sistema.** 🎉

Ejecuta `python main.py` para comenzar.
