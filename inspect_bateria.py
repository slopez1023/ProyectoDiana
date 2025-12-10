"""
Script para inspeccionar el archivo de batería de indicadores sectoriales
"""

import pandas as pd

archivo = r"C:\Users\santi\TableroIndicadores\63721_bateria-indicadores-sectoriales.xlsx"

print("Analizando archivo de batería de indicadores...")
print("=" * 80)

# Obtener todas las hojas
xl_file = pd.ExcelFile(archivo)
hojas = xl_file.sheet_names

print(f"\n✅ Archivo encontrado con {len(hojas)} hojas\n")
print("=" * 80)
print("LISTADO DE HOJAS:")
print("=" * 80)

for i, hoja in enumerate(hojas, 1):
    print(f"{i}. {hoja}")

print("\n" + "=" * 80)
print("ANALIZANDO ESTRUCTURA DE CADA HOJA:")
print("=" * 80)

for hoja in hojas:
    print(f"\n{'='*80}")
    print(f"HOJA: {hoja}")
    print('='*80)
    
    try:
        # Leer sin encabezados para ver la estructura
        df = pd.read_excel(archivo, sheet_name=hoja, header=None, nrows=10)
        
        print(f"Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
        print("\nPrimeras 5 filas:")
        
        for i in range(min(5, len(df))):
            print(f"\nFila {i}:")
            valores = df.iloc[i].tolist()
            # Mostrar solo primeros 5 valores para no saturar
            print(valores[:min(5, len(valores))])
            if len(valores) > 5:
                print(f"  ... y {len(valores) - 5} columnas más")
                
    except Exception as e:
        print(f"Error al leer hoja: {e}")

print("\n" + "=" * 80)
print("ANÁLISIS COMPLETO")
print("=" * 80)
