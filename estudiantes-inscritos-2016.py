import pandas as pd

# funciones
def sumarInscritos(data):

    return data['Inscritos 2016'].sum()


def filtarMunicipio(data,muni): 
    '''
    Filtra datafrema por municipios
    '''
    for i in range(len(data)): 
        return data.loc[data['Municipio de oferta del programa'] == muni]

def filtarDepartamento(data,depar):
    '''
    Filtra datafrema por departamentos
    '''
    for i in range(len(data)):#Departamento de oferta del programa
        return data.loc[data['Departamento de oferta del programa'] == depar]
    

# Carga información y salta filas 
df = pd.read_excel('add/inscritos_2016.xlsx', skiprows=[0,1,2,3,4,5])

# Nombres de las columnas
NOMBRE_COLUNMAS = df.columns
# Limpiar nombre de colunmas colNombres
NOMBRE_COLUMNAS_NUEVOS = NOMBRE_COLUNMAS.str.replace('\n', '')
# renombrando columnas
df.columns = NOMBRE_COLUMNAS_NUEVOS
# correcion de nombres (casos puntuales)
df = df.rename(columns={'Principal oSeccional':'Principal o Seccional','Municipio dedomicilio de la IES':'Municipio de domicilio de la IES','Código SNIES delprograma':'Código SNIES del programa'})

# Contar campos vacios por columnas
print( df.index, df.isnull().sum() )

# Mostrar filas duplicadas
filasDuplicadas = df[df.duplicated()]
print("\nLas filas duplicadas son: ")
print(filasDuplicadas)

# Lista de departamentos relacionada en el dataframe
DEPARTAMENTOS = pd.unique(df['Departamento de oferta del programa']).tolist()
                              #Departamento de oferta del programa

# Lista de municipios relacionados en en dataframe
MUNICIPIOS = pd.unique(df['Municipio de oferta del programa']).tolist()
# print(DEPARTAMENTOS)

# Dataframe de estudiantes
df_estudiantes = df.iloc[:,25:33]
# print(df_estudiantes)

# Numero total de personas incritas en 2016
TOTAL_INSCRITOS_2016 = sumarInscritos(df_estudiantes)
# inscritos por departamento
TOTAL_INSCRITOS_X_DEPARTAMENTOS = [ sumarInscritos( filtarDepartamento(df_estudiantes,DEPARTAMENTOS[i])) for i in range( len(DEPARTAMENTOS) ) ]
# inscritos por municipio
TOTAL_INSCRITOS_X_MUNICIPIOS = [ sumarInscritos( filtarMunicipio( df_estudiantes,MUNICIPIOS[i])) for i in range( len(MUNICIPIOS) ) ]

inscritosDepartamentos = pd.DataFrame( list(zip(DEPARTAMENTOS, TOTAL_INSCRITOS_X_DEPARTAMENTOS)), columns=["Departamentos", "Total de inscritos"])
inscritosMunicipio = pd.DataFrame( list(zip(MUNICIPIOS, TOTAL_INSCRITOS_X_MUNICIPIOS)), columns=["Municipios","Total de inscritos"])

print(inscritosDepartamentos)
print(inscritosMunicipio)
