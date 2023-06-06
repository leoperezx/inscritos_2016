import pandas as pd
import add.funciones as fn


# Carga información y salta filas 
df = pd.read_excel('add/inscritos_2016.xlsx', skiprows=[0,1,2,3,4,5])

# Limpiar nombre de colunmas
nombresColumnas = df.columns
nombresColumnasNuevos = fn.eliminar_nuevaLinea(nombresColumnas)
# renombrando columnas
df.columns = nombresColumnasNuevos

# Contar campos vacios por columnas
print(df.isnull().sum())

