"""
Script para ver TODOS los indicadores con sus valores de semaforización
"""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_processing.excel_loader import load_and_process_excel

archivo_excel = r"C:\Users\santi\TableroIndicadores\RE-SM-01 Tablero de Control de Indicadores 2025.xls"

print("Cargando indicadores...")
df, indicadores, resumen = load_and_process_excel(archivo_excel)

print(f"\nTotal de indicadores: {len(indicadores)}")
print("\n" + "=" * 120)
print(f"{'#':<3} {'Nombre':<50} {'Meta':<8} {'N.Obt':<8} {'N.Sat':<8} {'N.Crit':<8} {'Últ.Val':<10}")
print("=" * 120)

meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
              'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

for i, ind in enumerate(indicadores, 1):
    nombre = str(ind['nombre'])[:48]
    meta = ind.get('meta', 'N/A')
    n_obt = ind.get('nivel_obtenido', 'N/A')
    n_sat = ind.get('nivel_satisfactorio', 'N/A')
    n_crit = ind.get('nivel_critico', 'N/A')
    
    # Formatear valores
    meta_str = f"{meta:.4f}" if pd.notna(meta) else "N/A"
    n_obt_str = f"{n_obt:.4f}" if pd.notna(n_obt) else "N/A"
    n_sat_str = f"{n_sat:.4f}" if pd.notna(n_sat) else "N/A"
    n_crit_str = f"{n_crit:.4f}" if pd.notna(n_crit) else "N/A"
    
    # Último valor
    valores_mensuales = ind.get('valores_mensuales', {})
    ultimo_valor = None
    if valores_mensuales:
        for mes in reversed(meses_orden):
            if mes in valores_mensuales:
                ultimo_valor = valores_mensuales[mes]
                break
    
    ultimo_val_str = f"{ultimo_valor:.4f}" if ultimo_valor is not None else "N/A"
    
    print(f"{i:<3} {nombre:<50} {meta_str:<8} {n_obt_str:<8} {n_sat_str:<8} {n_crit_str:<8} {ultimo_val_str:<10}")
