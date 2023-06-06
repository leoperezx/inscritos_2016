import pandas as pd

# funciones
def sumarInscritos(data):

    return data['Inscritos 2016'].sum()


def filtarMunicipio(data,muni): 
    
    for i in range(len(data)):
        return data.loc[data['Municipio de oferta del programa'] == muni]


# Carga información y salta filas 
df = pd.read_excel('add/inscritos_2016.xlsx', skiprows=[0,1,2,3,4,5])

# Nombres de las columnas
NOMBRE_COLUNMAS = df.columns
# Limpiar nombre de colunmas colNombres
NOMBRE_COLUMNAS_NUEVOS = NOMBRE_COLUNMAS.str.replace('\n', '')
# renombrando columnas
df.columns = NOMBRE_COLUMNAS_NUEVOS
# correcion de nombres
df = df.rename(columns={'Principal oSeccional':'Principal o Seccional','Municipio dedomicilio de la IES':'Municipio de domicilio de la IES','Código SNIES delprograma':'Código SNIES del programa'})

# Contar campos vacios por columnas
print( df.index, df.isnull().sum() )

# Mostrar filas duplicadas
filasDuplicadas = df[df.duplicated()]
print("\nLas filas duplicadas son: ")
print(filasDuplicadas)

# Lista de municipios relacionados en en dataframe
MUNICIPIOS = pd.unique(df['Municipio de oferta del programa']).tolist()
# print(MUNICIPIOS.tolist())

# Dataframe de estudiantes
df_estudiantes = df.iloc[:,27:33]
print(df_estudiantes.head())
TOTAL_INSCRITOS_2016 = sumarInscritos(df_estudiantes)

TOTAL_INSCRITOS_BOGOTA = sumarInscritos( filtarMunicipio( df_estudiantes,'Bogota' ) )
print(range(len(MUNICIPIOS)))

# inscritos por municipio
TOTAL_INSCRITOS_X_MUNICIPIOS = [ sumarInscritos( filtarMunicipio( df_estudiantes,MUNICIPIOS[i])) for i in range( len(MUNICIPIOS) ) ]


InscritosMunicipio = pd.DataFrame( list(zip(MUNICIPIOS, TOTAL_INSCRITOS_X_MUNICIPIOS)), columns=["Municipios","Total de inscritos"])
# print(TOTAL_INSCRITOS_X_MUNICIPIOS)
# print(MUNICIPIOS)
print(InscritosMunicipio)