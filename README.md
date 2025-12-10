# Sistema de Tablero de Control de Indicadores MIPG

## 📋 Descripción

Sistema integral de análisis y visualización de indicadores institucionales bajo lineamientos MIPG (Modelo Integrado de Planeación y Gestión) para la Secretaría de Planeación de una entidad territorial.

## ✨ Características Principales

- ✅ **Importación automática** de datos desde Excel
- 📊 **Clasificación inteligente** de periodicidad de indicadores (mensual, trimestral, semestral, anual)
- 🎯 **Semaforización automática** según criterios de cumplimiento
- 📈 **Análisis de tendencias** (crecimiento, estabilidad, retroceso, volatilidad)
- ⚠️ **Detección de anomalías** mediante análisis estadístico (Z-score)
- 📄 **Generación automática** de reportes PDF ejecutivos
- 🖥️ **Dashboard interactivo** con Streamlit
- 🔍 **Filtros avanzados** por periodicidad, estado y tendencia
- 📉 **Visualizaciones interactivas** con Plotly

## 🏗️ Arquitectura del Proyecto

```
TableroIndicadores/
│
├── src/                              # Código fuente del sistema
│   ├── data_processing/              # Módulo de procesamiento de datos
│   │   ├── __init__.py
│   │   └── excel_loader.py          # Carga y limpieza de datos Excel
│   │
│   ├── analysis/                     # Módulo de análisis de indicadores
│   │   ├── __init__.py
│   │   └── indicator_analyzer.py    # Análisis, clasificación y tendencias
│   │
│   ├── visualization/                # Módulo de visualización
│   │   ├── __init__.py
│   │   └── chart_generator.py       # Generación de gráficos Plotly
│   │
│   ├── reporting/                    # Módulo de reportes
│   │   ├── __init__.py
│   │   └── report_generator.py      # Generación de PDF con ReportLab
│   │
│   ├── utils/                        # Utilidades del sistema
│   │   ├── __init__.py
│   │   ├── config.py                # Configuración global
│   │   └── helpers.py               # Funciones auxiliares
│   │
│   ├── dashboard.py                  # Aplicación Streamlit
│   └── __init__.py
│
├── data/                             # Datos del proyecto
│   ├── input/                        # Archivos de entrada
│   └── processed/                    # Datos procesados
│
├── output/                           # Resultados generados
│   ├── reports/                      # Reportes PDF
│   └── charts/                       # Gráficos generados
│
├── tests/                            # Pruebas unitarias
├── docs/                             # Documentación adicional
├── config/                           # Archivos de configuración
│
├── main.py                           # Script principal
├── requirements.txt                  # Dependencias Python
├── README.md                         # Este archivo
└── RE-SM-01 Tablero de Control de Indicadores 2025.xls
```

## 🔧 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv .venv
```

3. **Activar entorno virtual**

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 🚀 Uso del Sistema

### 1. Ejecución Completa del Análisis

Procesa el archivo Excel, genera análisis, gráficos y reportes:

```bash
python main.py
```

Este comando ejecuta:
- Carga y limpieza de datos
- Análisis de todos los indicadores
- Generación de gráficos interactivos
- Creación de reporte PDF ejecutivo

### 2. Dashboard Interactivo

Para abrir el dashboard web interactivo:

```bash
streamlit run src/dashboard.py
```

El dashboard se abrirá automáticamente en su navegador (http://localhost:8501)

### 3. Uso Programático

También puede importar y usar los módulos directamente:

```python
from src.data_processing.excel_loader import load_and_process_excel
from src.analysis.indicator_analyzer import analizar_todos_indicadores
from src.visualization.chart_generator import ChartGenerator

# Cargar datos
df, indicadores, resumen = load_and_process_excel("archivo.xls")

# Analizar
analisis = analizar_todos_indicadores(indicadores)

# Generar gráfico
generator = ChartGenerator()
fig = generator.grafico_tendencia_indicador(indicadores[0], analisis[0])
fig.show()
```

## 📊 Funcionalidades del Dashboard

### Página de Inicio
- Métricas generales de todos los indicadores
- Distribución de semaforización (Verde/Amarillo/Rojo)
- Gráficos comparativos
- Tendencias múltiples

### Explorar Indicadores
- Filtros por:
  - Periodicidad (Mensual, Trimestral, etc.)
  - Estado de semáforo
  - Tipo de tendencia
  - Búsqueda por texto
- Detalle completo de cada indicador:
  - Gráfico de tendencia temporal
  - Interpretación automática
  - Estadísticas detalladas
  - Anomalías detectadas
  - Valores por período

### Generar Reportes
- Configuración de opciones del reporte
- Selección de indicadores a incluir
- Generación de PDF ejecutivo
- Descarga del archivo generado

## 📖 Módulos Principales

### 1. ExcelDataLoader (`excel_loader.py`)

**Responsabilidad**: Carga, validación y limpieza de datos Excel.

**Funciones clave**:
- `load_data()`: Carga el archivo Excel
- `validate_structure()`: Valida la estructura esperada
- `clean_data()`: Limpia y normaliza datos
- `extract_indicators_data()`: Extrae información estructurada

**Principios SOLID aplicados**:
- Single Responsibility: Solo se encarga de la carga de datos
- Open/Closed: Extensible para nuevos formatos

### 2. IndicatorAnalyzer (`indicator_analyzer.py`)

**Responsabilidad**: Análisis completo de indicadores MIPG.

**Funciones clave**:
- `clasificar_periodicidad()`: Identifica automáticamente la periodicidad
- `calcular_semaforo()`: Determina el estado del indicador
- `analizar_tendencia()`: Calcula tendencias mediante regresión lineal
- `detectar_anomalias()`: Identifica valores atípicos con Z-score
- `calcular_estadisticas()`: Estadística descriptiva completa

**Algoritmos implementados**:
- Regresión lineal simple para tendencias
- Z-score para detección de anomalías (umbral: ±2.5)
- Coeficiente de variación para volatilidad

### 3. ChartGenerator (`chart_generator.py`)

**Responsabilidad**: Generación de visualizaciones interactivas.

**Tipos de gráficos**:
- Tendencia temporal individual
- Comparativo de múltiples indicadores
- Distribución de semaforización (pie chart)
- Tendencias múltiples superpuestas
- Estadísticas generales (box plots)

**Tecnología**: Plotly para gráficos interactivos HTML

### 4. PDFReportGenerator (`report_generator.py`)

**Responsabilidad**: Generación de reportes ejecutivos en PDF.

**Secciones del reporte**:
1. Portada institucional
2. Resumen ejecutivo
3. Análisis por periodicidad
4. Análisis de tendencias
5. Indicadores críticos
6. Recomendaciones automáticas

**Tecnología**: ReportLab para generación de PDF

## 🎯 Criterios de Semaforización

El sistema aplica los siguientes criterios para determinar el estado:

- 🟢 **Verde (Satisfactorio)**: Valor actual >= Nivel satisfactorio
- 🟡 **Amarillo (Alerta)**: Nivel crítico <= Valor actual < Nivel satisfactorio
- 🔴 **Rojo (Crítico)**: Valor actual < Nivel crítico
- ⚪ **Gris (Sin datos)**: Datos insuficientes

## 📈 Clasificación de Tendencias

Mediante análisis de regresión lineal:

- **Crecimiento**: Pendiente positiva significativa (> 0.5)
- **Estabilidad**: Pendiente cercana a cero (|pendiente| < 0.5)
- **Retroceso**: Pendiente negativa significativa (< -0.5)
- **Volátil**: Coeficiente de variación > 15%
- **Datos Insuficientes**: Menos de 2 períodos con datos

## ⚠️ Detección de Anomalías

El sistema utiliza el método de **Z-score** para identificar valores atípicos:

```
Z-score = (valor - media) / desviación_estándar
```

- Anomalía si |Z-score| > 2.5
- Clasifica como "Alto" o "Bajo"
- Calcula desviación porcentual respecto a la media

## 🔍 Periodicidades Soportadas

El sistema detecta automáticamente:

- **Mensual**: Datos cada mes
- **Bimestral**: Datos cada 2 meses
- **Trimestral**: Datos cada 3 meses
- **Cuatrimestral**: Datos cada 4 meses
- **Semestral**: Datos cada 6 meses
- **Anual**: Datos anuales

## 📝 Formato del Archivo Excel

El archivo debe contener:

**Columnas requeridas**:
- `Nombre del Indicador`: Nombre descriptivo
- `Meta`: Meta establecida (%)
- Columnas de meses: `Enero`, `Febrero`, ..., `Diciembre`

**Columnas opcionales (para semaforización)**:
- `Nivel Obtenido`: Nivel actual
- `Nivel Satisfactorio`: Umbral para verde
- `Nivel Crítico`: Umbral para rojo

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.12+ | Lenguaje principal |
| Pandas | 2.1+ | Procesamiento de datos |
| Streamlit | 1.28+ | Dashboard interactivo |
| Plotly | 5.17+ | Gráficos interactivos |
| ReportLab | 4.0+ | Generación de PDF |
| NumPy | 1.24+ | Cálculos numéricos |
| Matplotlib | 3.8+ | Visualizaciones base |
| Seaborn | 0.13+ | Gráficos estadísticos |

## 📚 Principios de Desarrollo

### Principios SOLID Aplicados

1. **Single Responsibility**: Cada clase tiene una única responsabilidad
   - `ExcelDataLoader`: Solo carga datos
   - `IndicatorAnalyzer`: Solo analiza
   - `ChartGenerator`: Solo genera gráficos

2. **Open/Closed**: Extensible sin modificar código existente
   - Nuevos tipos de análisis pueden agregarse
   - Nuevos formatos de visualización

3. **Liskov Substitution**: Interfaces consistentes

4. **Interface Segregation**: Funciones específicas y modulares

5. **Dependency Inversion**: Depende de abstracciones, no de implementaciones concretas

### Buenas Prácticas Implementadas

- ✅ **Docstrings completos** en todas las funciones
- ✅ **Type hints** para parámetros y retornos
- ✅ **Logging estructurado** para trazabilidad
- ✅ **Manejo de errores** con try-except
- ✅ **Validaciones de datos** en cada etapa
- ✅ **Código modular** y reutilizable
- ✅ **Nombres descriptivos** de variables y funciones
- ✅ **Cumplimiento PEP 8** (estándar de estilo Python)

## 🔐 Consideraciones de Seguridad

- Los datos se procesan localmente
- No se envía información a servicios externos
- Los archivos generados se almacenan localmente
- Validación de entrada de datos para prevenir errores

## 📊 Salidas del Sistema

### 1. Archivos Generados

**Gráficos HTML** (`output/charts/`):
- `semaforizacion_general.html`: Distribución de estados
- `comparativo_indicadores.html`: Comparación top 10
- `tendencias_multiples.html`: Tendencias superpuestas
- `estadisticas_generales.html`: Estadísticas visuales

**Reportes PDF** (`output/reports/`):
- `Informe_Indicadores_MIPG_[timestamp].pdf`: Reporte ejecutivo completo

**Logs** (raíz):
- `sistema_indicadores.log`: Registro de ejecuciones

### 2. Dashboard Web

Accesible en `http://localhost:8501` al ejecutar Streamlit.

## 🐛 Solución de Problemas

### Error: "Archivo no encontrado"

**Causa**: El archivo Excel no está en la ubicación correcta.

**Solución**: 
```bash
# Coloque el archivo en el directorio raíz:
TableroIndicadores/RE-SM-01 Tablero de Control de Indicadores 2025.xls
```

### Error: "ModuleNotFoundError"

**Causa**: Dependencias no instaladas.

**Solución**:
```bash
pip install -r requirements.txt
```

### Error al generar PDF

**Causa**: Falta instalar ReportLab o sus dependencias.

**Solución**:
```bash
pip install reportlab Pillow
```

### Dashboard no se abre

**Causa**: Puerto ocupado o Streamlit no instalado.

**Solución**:
```bash
# Reinstalar Streamlit
pip install --upgrade streamlit

# Usar puerto alternativo
streamlit run src/dashboard.py --server.port 8502
```

## 📞 Soporte y Contacto

Para soporte técnico o consultas sobre el sistema, contacte a:

**Secretaría de Planeación**  
Área MIPG – Política de Gestión de la Información y Análisis de Datos

## 📄 Licencia

Este sistema es de uso interno para la entidad territorial.

## 📅 Versión

**v1.0.0** - Diciembre 2025

---

## 🎓 Documentación Técnica Adicional

### Flujo de Datos

```
Excel → ExcelDataLoader → DataFrame limpio
           ↓
      IndicatorAnalyzer → Análisis completo
           ↓
      ┌────┴─────┬────────────┐
      ↓          ↓            ↓
ChartGenerator  Dashboard  PDFReport
      ↓          ↓            ↓
   HTML       Streamlit     PDF
```

### Estructura de Datos

**Indicador (Dict)**:
```python
{
    'id': int,
    'nombre': str,
    'meta': float,
    'valores_mensuales': Dict[str, float],
    'nivel_obtenido': float,
    'nivel_satisfactorio': float,
    'nivel_critico': float
}
```

**Análisis (Dict)**:
```python
{
    'indicador_id': int,
    'nombre': str,
    'periodicidad': str,
    'tendencia': str,
    'pendiente': float,
    'semaforo': str,
    'estadisticas': Dict,
    'anomalias': List[Dict],
    'interpretacion': str
}
```

---

**Desarrollado con 💙 para la Secretaría de Planeación**
