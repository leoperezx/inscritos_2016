import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    
def filtrarPrograma(data,programa):
    '''
    Filtra por programa
    '''
    for i in range(len(data)):
        return data.loc[data['Programa Académico'] == programa]

# Carga información y salta filas 
df = pd.read_excel('add/inscritos_2016.xlsx', skiprows=[0,1,2,3,4,5])

# Nombres de las columnas
NOMBRE_COLUNMAS = df.columns
# Limpiar nombre de colunmas colNombres
NOMBRE_COLUMNAS_NUEVOS = NOMBRE_COLUNMAS.str.replace('\n', '')
# renombrando columnas
df.columns = NOMBRE_COLUMNAS_NUEVOS
# correcion de nombres (casos puntuales)
df = df.rename(columns={'Principal oSeccional':'Principal o Seccional',
                        'Municipio dedomicilio de la IES':'Municipio de domicilio de la IES',
                        'Código SNIES delprograma':'Código SNIES del programa'})

# Contar campos vacios por columnas
print( df.index, df.isnull().sum() )

# Mostrar filas duplicadas
filasDuplicadas = df[df.duplicated()]
print("\nLas filas duplicadas son: ")
print(filasDuplicadas)

# Lista de departamentos relacionada en el dataset
DEPARTAMENTOS = pd.unique(df['Departamento de oferta del programa']).tolist()

# Lista de municipios relacionados en el dataset
MUNICIPIOS = pd.unique(df['Municipio de oferta del programa']).tolist()

# Lista de programas
PROGRAMAS = pd.unique(df['Programa Académico']).tolist()

# lista de sexos relacionados en el dataset 
# SEXO = pd.unique(df['Sexo']).tolist()
# print(SEXO)

# Dataframe de estudiantes
df_estudiantes = df.iloc[:,25:33]
# print(df_estudiantes)

# Numero total de personas incritas en 2016
TOTAL_INSCRITOS_2016 = sumarInscritos(df_estudiantes)
print("Total de inscritos: \n", TOTAL_INSCRITOS_2016)

# inscritos por departamento
INSCRITOS_X_DEPARTAMENTOS = [ sumarInscritos( filtarDepartamento(df_estudiantes,DEPARTAMENTOS[i])) for i in range( len(DEPARTAMENTOS) ) ]
# inscritos por municipio
INSCRITOS_X_MUNICIPIOS = [ sumarInscritos( filtarMunicipio( df_estudiantes,MUNICIPIOS[i])) for i in range( len(MUNICIPIOS) ) ]

df_Male_Filter = df["Sexo"] == "HOMBRE"
df_Male = df[df_Male_Filter]

df_Female_Filter = df["Sexo"] == "MUJER"
df_Female = df[df_Female_Filter]

MALE_X_DEPARTAMENTOS = [ sumarInscritos( filtarDepartamento(df_Male,DEPARTAMENTOS[i])) for i in range( len(DEPARTAMENTOS) ) ]
FEMALE_X_DEPARTAMENTOS = [ sumarInscritos( filtarDepartamento(df_Female,DEPARTAMENTOS[i])) for i in range( len(DEPARTAMENTOS) ) ]

MALE_X_MUNICIPIOS = [ sumarInscritos( filtarMunicipio( df_Male,MUNICIPIOS[i])) for i in range( len(MUNICIPIOS) ) ]
FEMALE_X_MUNICIPIOS = [ sumarInscritos( filtarMunicipio( df_Female,MUNICIPIOS[i])) for i in range( len(MUNICIPIOS) ) ]

inscritosDepartamentos = pd.DataFrame( list(zip(DEPARTAMENTOS,MALE_X_DEPARTAMENTOS,FEMALE_X_DEPARTAMENTOS,INSCRITOS_X_DEPARTAMENTOS)), 
                                      columns=["Departamentos","Hombres","Mujeres","Inscritos"])

inscritosMunicipio = pd.DataFrame( list(zip(MUNICIPIOS,MALE_X_MUNICIPIOS,FEMALE_X_MUNICIPIOS, INSCRITOS_X_MUNICIPIOS)), 
                                  columns=["Municipios","Hombres","Mujeres", "Inscritos"])

inscritosDepartamentos["Porcentaje_inscritos"] = ((inscritosDepartamentos["Inscritos"]/TOTAL_INSCRITOS_2016)*100)
inscritosDepartamentos["Porcentaje_hombres"] = ((inscritosDepartamentos["Hombres"]/inscritosDepartamentos["Inscritos"])*100)
inscritosDepartamentos["Porcentaje_mujeres"] = ((inscritosDepartamentos["Mujeres"]/inscritosDepartamentos["Inscritos"])*100)

inscritosMunicipio["Porcentaje_inscritos"] = (inscritosMunicipio["Inscritos"]/TOTAL_INSCRITOS_2016)*100
inscritosMunicipio["Porcentaje_hombres"] = (inscritosMunicipio["Hombres"]/inscritosMunicipio["Inscritos"])*100
inscritosMunicipio["Porcentaje_mujeres"] = (inscritosMunicipio["Mujeres"]/inscritosMunicipio["Inscritos"])*100

# IND = df["Programa Académico"].str.contains('TÉCNICA','TÉCNICO', regex=True)
# df_tecnico = df[IND]
# print( pd.unique(df_tecnico["Programa Académico"]).tolist() )

# Gráficas
#grafica_municipios1 = inscritosDepartamentos[["Departamentos","Inscritos","Hombres","Mujeres"]]
#fig1 = px.bar(grafica_municipios1, x="Departamentos", y=["Hombres","Mujeres"], title="Inscritos por Departamento")
#fig1.write_html('first_figure.html', auto_open=True)

grafica_municipios2 = inscritosMunicipio[["Municipios","Porcentaje_hombres","Porcentaje_mujeres"]]
#print((grafica_municipios2[grafica_municipios2["Municipios"] == "Bogota"]))

fig3 = go.Figure(data=[go.Table(header=dict(values=list(grafica_municipios2.columns),
                                            fill_color='paleturquoise',
                                            align='left'),
                                cells=dict(values=[grafica_municipios2.Municipios, grafica_municipios2.Porcentaje_hombres,grafica_municipios2.Porcentaje_mujeres],
                                          fill_color='lavender',
                                          align='left'))
                                          ])
fig3.update_layout(height=700, width=600, title="Inscritos por genero por Municipios [%]")
fig3.write_html('third_figure.html', auto_open=True)

#grafica_municipios2 = inscritosMunicipio[["Municipios","Porcentaje_hombres","Porcentaje_mujeres"]]
#fig2 = make_subplots(rows=2,cols=2, 
#                     specs=[[{"type": "domain"}, {"type": "domain"}],[{"type": "domain"}, {"type": "domain"}]],
#                     subplot_titles=("Plot 1","Plot 2","Plot 3","Plot 4"))
#fig2.add_trace(go.Pie(values=(grafica_municipios2["Municipios"] == "Bogota").tolist() ), row=1,col=1)
#fig2.add_trace(go.Pie(values=(grafica_municipios2["Municipios"] == "Medellin").tolist() ), row=2,col=1)
#fig2.add_trace(go.Pie(values=(grafica_municipios2["Municipios"] == "Cali").tolist() ), row=1,col=2)
#fig2.add_trace(go.Pie(values=(grafica_municipios2["Municipios"] == "Palmira").tolist() ), row=2,col=2)
#fig2.update_layout(height=700, width=700, title="Porcentajes de inscritos por genero de ciudades importantes")
#names = {'Plot 1':'Bogotá', 'Plot 2':'Medellín', 'Plot 3':'Cali', 'Plot 4':'Palmira'}
#fig2.for_each_annotation(lambda a: a.update(text = a.text + ': ' + names[a.text]))
#fig2.write_html('second_figure.html', auto_open=True)