import pandas as pd

# Carga información y salta filas 
df = pd.read_excel('add/inscritos_2016.xlsx', skiprows=[0,1,2,3,4,5])

# Nombres de las columnas
nombresColumnas = df.columns
# Limpiar nombre de colunmas colNombres
nombresColumnasNuevos = nombresColumnas.str.replace('\n', '')
# renombrando columnas
df.columns = nombresColumnasNuevos

# Contar campos vacios por columnas
print(df.isnull().sum())

# Mostrar filas duplicadas
filasDuplicadas = df[df.duplicated()]
print("\nLas filas duplicadas son: ")
print(filasDuplicadas)
