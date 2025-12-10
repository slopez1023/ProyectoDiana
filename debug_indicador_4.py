"""
Debug específico del indicador 4 (PQRS Vencidos)
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_processing.excel_loader import load_and_process_excel
from analysis.indicator_analyzer import IndicatorAnalyzer

archivo_excel = r"C:\Users\santi\TableroIndicadores\RE-SM-01 Tablero de Control de Indicadores 2025.xls"

df, indicadores, resumen = load_and_process_excel(archivo_excel)

# Indicador 4 (index 3)
ind = indicadores[3]

print("=" * 80)
print("INDICADOR 4: PQRS Vencidos")
print("=" * 80)
print(f"Nombre: {ind['nombre']}")
print(f"Meta: {ind.get('meta')}")
print(f"Nivel Obtenido: {ind.get('nivel_obtenido')}")
print(f"Nivel Satisfactorio: {ind.get('nivel_satisfactorio')}")
print(f"Nivel Crítico: {ind.get('nivel_critico')}")
print(f"Valores mensuales: {ind.get('valores_mensuales')}")
print(f"Promedio: {ind.get('promedio')}")

# Simular el cálculo de semáforo
analyzer = IndicatorAnalyzer()

valores_mensuales = ind.get('valores_mensuales', {})
ultimo_valor = None
meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
              'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

for mes in reversed(meses_orden):
    if mes in valores_mensuales and pd.notna(valores_mensuales[mes]):
        ultimo_valor = valores_mensuales[mes]
        print(f"\nÚltimo valor encontrado en {mes}: {ultimo_valor}")
        break

if ultimo_valor is None and valores_mensuales:
    valores_lista = [v for v in valores_mensuales.values() if pd.notna(v)]
    if valores_lista:
        ultimo_valor = np.mean(valores_lista)
        print(f"\nNo hay último valor, usando promedio: {ultimo_valor}")

print(f"\nValor para semaforización: {ultimo_valor}")
print(f"¿Es None?: {ultimo_valor is None}")
print(f"¿Es nan?: {pd.isna(ultimo_valor) if ultimo_valor is not None else 'N/A'}")

semaforo = analyzer.calcular_semaforo(
    ultimo_valor if ultimo_valor is not None else np.nan,
    ind.get('meta', np.nan),
    ind.get('nivel_satisfactorio', np.nan),
    ind.get('nivel_critico', np.nan),
    ind.get('nivel_obtenido', np.nan)
)

print(f"\n>>> RESULTADO SEMÁFORO: {semaforo.value}")
