"""
Script para inspeccionar las primeras filas del Excel y encontrar los encabezados
"""

import pandas as pd

archivo_excel = r"C:\Users\santi\TableroIndicadores\RE-SM-01 Tablero de Control de Indicadores 2025.xls"

print("Leyendo archivo sin procesar...")
print("=" * 80)

# Leer sin asumir encabezados
df_raw = pd.read_excel(archivo_excel, header=None, engine='xlrd')

print(f"Dimensiones: {df_raw.shape}")
print("\nPrimeras 10 filas del archivo:")
print("=" * 80)

for i in range(min(10, len(df_raw))):
    print(f"\nFila {i}:")
    print(df_raw.iloc[i].tolist())

print("\n" + "=" * 80)
print("Buscando fila con encabezados...")
print("=" * 80)

# Buscar la fila que tiene "Nombre del Indicador" o similar
for i in range(min(15, len(df_raw))):
    row_values = df_raw.iloc[i].astype(str).tolist()
    row_text = ' '.join(row_values).lower()
    
    if 'indicador' in row_text or 'meta' in row_text or 'enero' in row_text:
        print(f"\n✅ Posible fila de encabezados encontrada en fila {i}:")
        print(df_raw.iloc[i].tolist())
