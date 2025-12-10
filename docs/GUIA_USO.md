# Guía de Uso del Sistema de Tablero de Indicadores MIPG

## Inicio Rápido

### 1. Preparación Inicial

**Requisitos previos:**
- Python 3.8 o superior instalado
- Archivo Excel con indicadores en el directorio raíz

**Pasos:**

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Verificar que el archivo Excel esté presente
# Debe estar en: TableroIndicadores/RE-SM-01 Tablero de Control de Indicadores 2025.xls

# 3. Ejecutar el sistema completo
python main.py

# 4. Abrir el dashboard interactivo
streamlit run src/dashboard.py
```

### 2. Ejecución del Análisis Completo

El script `main.py` ejecuta automáticamente:

```
✓ Carga de datos desde Excel
✓ Validación y limpieza
✓ Análisis de todos los indicadores
✓ Generación de gráficos interactivos
✓ Creación de reporte PDF ejecutivo
```

**Salida esperada:**
```
================================================================================
SISTEMA DE TABLERO DE CONTROL DE INDICADORES MIPG
Secretaría de Planeación
================================================================================

[PASO 1/5] Cargando y procesando datos del Excel...
✓ Datos cargados exitosamente
  - Total indicadores procesados: XX
  - Dimensiones DataFrame: (XX, XX)

[PASO 2/5] Analizando indicadores...
✓ Análisis completado
  - Indicadores en estado satisfactorio (Verde): XX
  - Indicadores en estado alerta (Amarillo): XX
  - Indicadores en estado crítico (Rojo): XX

[PASO 3/5] Generando gráficos...
✓ Gráficos generados: 4
  - semaforizacion_general: output/charts/semaforizacion_general.html
  - comparativo: output/charts/comparativo_indicadores.html
  - tendencias_multiples: output/charts/tendencias_multiples.html
  - estadisticas: output/charts/estadisticas_generales.html

[PASO 4/5] Generando informe PDF...
✓ Reporte PDF generado: output/reports/Informe_Indicadores_MIPG_XXXXXX.pdf

[PASO 5/5] Proceso completado exitosamente
```

## Uso del Dashboard Interactivo

### 1. Iniciar el Dashboard

```bash
streamlit run src/dashboard.py
```

El dashboard se abrirá en su navegador en `http://localhost:8501`

### 2. Navegación por el Dashboard

#### Página de Inicio 🏠

**Contenido:**
- Métricas generales (total indicadores, estados)
- Gráficos de resumen:
  - Distribución de semaforización
  - Comparativo de indicadores
  - Tendencias múltiples

**Uso:**
- Ver panorama general del estado institucional
- Identificar rápidamente áreas de atención
- Analizar distribución de cumplimiento

#### Página Explorar Indicadores 🔍

**Filtros disponibles:**

1. **Por Periodicidad:**
   - Todas
   - Mensual
   - Bimestral
   - Trimestral
   - Cuatrimestral
   - Semestral
   - Anual

2. **Por Estado Semáforo:**
   - Todos
   - Verde (Satisfactorio)
   - Amarillo (Alerta)
   - Rojo (Crítico)
   - Gris (Sin datos)

3. **Por Tendencia:**
   - Todas
   - Crecimiento
   - Estabilidad
   - Retroceso
   - Volátil
   - Datos Insuficientes

4. **Búsqueda por Texto:**
   - Ingrese palabras clave del nombre del indicador

**Detalle de Indicador:**

Al seleccionar un indicador, se muestra:
- **Información General:**
  - Periodicidad detectada
  - Meta establecida
  - Tendencia identificada
  - Promedio calculado
  - Estado del semáforo

- **Gráfico de Tendencia:**
  - Evolución temporal
  - Línea de meta (si aplica)
  - Valores por período
  - Interactivo (zoom, hover)

- **Interpretación Automática:**
  - Texto generado explicando el comportamiento
  - Recomendaciones basadas en análisis

- **Estadísticas Detalladas:**
  - Mínimo, máximo, mediana
  - Desviación estándar
  - Rango de valores
  - Coeficiente de variación

- **Anomalías Detectadas:**
  - Lista de valores atípicos
  - Z-score calculado
  - Desviación porcentual

- **Valores por Período:**
  - Tabla con todos los valores mensuales

#### Página Generar Reportes 📄

**Opciones del Reporte:**

1. **Contenido:**
   - ☑ Incluir gráficos
   - ☑ Incluir estadísticas detalladas
   - ☑ Incluir análisis de anomalías

2. **Nombre del archivo:**
   - Personalizable (default: Informe_Indicadores_MIPG)

3. **Filtros:**
   - Estados de semáforo a incluir
   - Número máximo de indicadores

**Proceso de Generación:**

1. Configurar opciones
2. Aplicar filtros deseados
3. Clic en "🎯 Generar Reporte PDF"
4. Esperar procesamiento
5. Descargar archivo generado

**Salida:**
- Archivo PDF en `output/reports/`
- Formato profesional institucional
- Listo para presentación

## Uso Programático

### 1. Importar y Usar Módulos

```python
# Ejemplo de uso programático del sistema

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_processing.excel_loader import load_and_process_excel
from analysis.indicator_analyzer import analizar_todos_indicadores, IndicatorAnalyzer
from visualization.chart_generator import ChartGenerator
from reporting.report_generator import generar_informe_pdf

# 1. CARGAR DATOS
print("Cargando datos...")
df, indicadores, resumen = load_and_process_excel("RE-SM-01 Tablero de Control de Indicadores 2025.xls")

print(f"Indicadores cargados: {len(indicadores)}")

# 2. ANALIZAR INDICADORES
print("Analizando indicadores...")
analisis = analizar_todos_indicadores(indicadores)

# 3. TRABAJAR CON UN INDICADOR ESPECÍFICO
indicador_ejemplo = indicadores[0]
analisis_ejemplo = analisis[0]

print(f"\nIndicador: {indicador_ejemplo['nombre']}")
print(f"Periodicidad: {analisis_ejemplo['periodicidad']}")
print(f"Tendencia: {analisis_ejemplo['tendencia']}")
print(f"Semáforo: {analisis_ejemplo['semaforo']}")

# 4. GENERAR GRÁFICO INDIVIDUAL
generator = ChartGenerator()
fig = generator.grafico_tendencia_indicador(indicador_ejemplo, analisis_ejemplo)

# Mostrar en navegador
fig.show()

# O guardar como HTML
generator.guardar_grafico(fig, "mi_grafico.html", formato="html")

# 5. GENERAR REPORTE PDF
print("\nGenerando reporte PDF...")
exito = generar_informe_pdf(
    indicadores,
    analisis,
    "mi_informe.pdf",
    titulo="Informe Personalizado",
    entidad="Mi Entidad"
)

if exito:
    print("✓ Reporte generado exitosamente")
```

### 2. Análisis Personalizado

```python
from analysis.indicator_analyzer import IndicatorAnalyzer

# Crear analizador
analyzer = IndicatorAnalyzer()

# Analizar periodicidad
valores = {
    'Enero': 85.5,
    'Febrero': 87.2,
    'Marzo': 86.8,
    'Abril': 88.1
    # ...
}

periodicidad = analyzer.clasificar_periodicidad(valores)
print(f"Periodicidad detectada: {periodicidad.value}")

# Calcular tendencia
tendencia, pendiente = analyzer.analizar_tendencia(valores)
print(f"Tendencia: {tendencia.value}, Pendiente: {pendiente:.2f}")

# Detectar anomalías
anomalias = analyzer.detectar_anomalias(valores)
print(f"Anomalías detectadas: {len(anomalias)}")

# Calcular estadísticas
stats = analyzer.calcular_estadisticas(valores)
print(f"Promedio: {stats['promedio']:.2f}")
print(f"Desviación: {stats['desviacion_estandar']:.2f}")
```

### 3. Generación de Gráficos Personalizados

```python
from visualization.chart_generator import ChartGenerator

generator = ChartGenerator(theme='plotly_white')

# Gráfico comparativo personalizado
fig_comp = generator.grafico_comparativo_indicadores(
    indicadores[:5],  # Solo primeros 5
    analisis[:5],
    top_n=5,
    ordenar_por='promedio'
)

fig_comp.show()

# Gráfico de semaforización
fig_sem = generator.grafico_semaforizacion_general(analisis)
fig_sem.show()

# Tendencias múltiples
fig_tend = generator.grafico_tendencias_multiple(indicadores, max_indicadores=3)
fig_tend.show()
```

## Interpretación de Resultados

### 1. Estados del Semáforo

| Color | Estado | Significado | Acción Requerida |
|-------|--------|-------------|------------------|
| 🟢 Verde | Satisfactorio | Cumple con la meta | Mantener el desempeño |
| 🟡 Amarillo | Alerta | Entre umbral crítico y meta | Seguimiento reforzado |
| 🔴 Rojo | Crítico | Por debajo del umbral | Acción inmediata |
| ⚪ Gris | Sin datos | Información insuficiente | Actualizar datos |

### 2. Tipos de Tendencia

**Crecimiento** (pendiente > 0.5):
- El indicador mejora sostenidamente
- Acciones implementadas están funcionando
- Mantener estrategias actuales

**Estabilidad** (|pendiente| < 0.5):
- Comportamiento constante
- Sin variaciones significativas
- Evaluar si se puede mejorar

**Retroceso** (pendiente < -0.5):
- Deterioro en el indicador
- Requiere análisis de causas
- Implementar acciones correctivas

**Volátil** (CV > 15%):
- Alta variabilidad en valores
- Comportamiento impredecible
- Revisar proceso de medición

### 3. Anomalías

**Z-score > 2.5**: Valor anormalmente alto
- Puede indicar:
  - Mejora excepcional
  - Error de captura
  - Evento especial

**Z-score < -2.5**: Valor anormalmente bajo
- Puede indicar:
  - Problema grave
  - Error de captura
  - Evento atípico

**Acción**: Verificar datos y contexto

### 4. Periodicidades

| Periodicidad | Frecuencia | Uso típico |
|--------------|------------|------------|
| Mensual | Cada mes | Indicadores operativos |
| Bimestral | Cada 2 meses | Seguimiento táctico |
| Trimestral | Cada 3 meses | Indicadores estratégicos |
| Semestral | Cada 6 meses | Evaluación semestral |
| Anual | Anual | Indicadores de impacto |

## Solución de Problemas Comunes

### Problema 1: Error al cargar Excel

**Síntoma:**
```
FileNotFoundError: No se encontró el archivo
```

**Solución:**
1. Verificar que el archivo esté en el directorio raíz
2. Verificar el nombre exacto del archivo
3. Verificar permisos de lectura

### Problema 2: Dashboard no carga datos

**Síntoma:**
- Página en blanco
- Error de carga

**Solución:**
```python
# Limpiar cache de Streamlit
streamlit cache clear

# Reiniciar el dashboard
streamlit run src/dashboard.py
```

### Problema 3: Gráficos no se generan

**Síntoma:**
- Gráficos vacíos
- Error al generar

**Solución:**
1. Verificar que haya datos válidos
2. Revisar logs en `sistema_indicadores.log`
3. Verificar instalación de Plotly:
```bash
pip install --upgrade plotly kaleido
```

### Problema 4: PDF no se genera

**Síntoma:**
```
Error al generar PDF
```

**Solución:**
```bash
# Reinstalar ReportLab y dependencias
pip install --upgrade reportlab Pillow
```

### Problema 5: Clasificación incorrecta de periodicidad

**Síntoma:**
- Periodicidad detectada no coincide con la real

**Solución:**
- Revisar que los datos estén completos
- Verificar que no haya vacíos irregulares
- Ajustar manualmente si es necesario

## Mejores Prácticas

### 1. Actualización de Datos

- Mantener el Excel actualizado mensualmente
- Verificar valores antes de cargar
- Documentar cambios significativos

### 2. Revisión de Análisis

- Revisar semanalmente el dashboard
- Analizar indicadores críticos primero
- Validar anomalías detectadas

### 3. Generación de Reportes

- Generar reportes mensuales para dirección
- Incluir análisis de tendencias
- Documentar acciones correctivas

### 4. Mantenimiento del Sistema

- Revisar logs periódicamente
- Limpiar archivos antiguos en `output/`
- Mantener backup del Excel original

## Preguntas Frecuentes (FAQ)

**P: ¿Puedo analizar varios archivos Excel?**  
R: Sí, cambie el nombre del archivo en `main.py` o use la función `load_and_process_excel()` con diferentes rutas.

**P: ¿Cómo exporto los gráficos?**  
R: Los gráficos se guardan automáticamente en `output/charts/`. También puede guardarlos desde el dashboard haciendo clic derecho → "Save as image".

**P: ¿Puedo personalizar los colores del semáforo?**  
R: Sí, edite el diccionario `COLORS_SEMAFORO` en `src/utils/config.py`.

**P: ¿Cómo agrego un nuevo tipo de análisis?**  
R: Cree un nuevo método en la clase `IndicatorAnalyzer` en `src/analysis/indicator_analyzer.py`.

**P: ¿El sistema funciona sin internet?**  
R: Sí, todo el procesamiento es local y no requiere conexión a internet.

**P: ¿Puedo modificar los umbrales de detección de anomalías?**  
R: Sí, ajuste `Z_SCORE_THRESHOLD` en `src/utils/config.py` (default: 2.5).

**P: ¿Cómo comparto los resultados?**  
R: Comparta los archivos PDF generados o los gráficos HTML desde la carpeta `output/`.

## Contacto y Soporte

Para soporte técnico o consultas:

**Secretaría de Planeación**  
Área MIPG – Política de Gestión de la Información y Análisis de Datos

---

**Versión de la Guía**: 1.0.0  
**Última Actualización**: Diciembre 2025
