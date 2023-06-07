# # Prueba de habilidad para el cargo de "analísta de datos"
# # en la Universidad Nacional de Colombia sede Bogotá.
# #
# # 
# # Contacto: leoeperez.x@gmail.com

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# #
# # funciones
# #
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
    for i in range(len(data)):
        return data.loc[data['Departamento de oferta del programa'] == depar]
    
def filtrarPrograma(data,programa):
    '''
    Filtra por programa
    '''
    for i in range(len(data)):
        return data.loc[data['Programa Académico'] == programa]

# #
# # Carga información y salta filas 
# #
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
# print(filasDuplicadas)

# Lista de departamentos relacionada en el dataset
DEPARTAMENTOS = pd.unique(df['Departamento de oferta del programa']).tolist()

# Lista de municipios relacionados en el dataset
MUNICIPIOS = pd.unique(df['Municipio de oferta del programa']).tolist()

# Lista de programas
PROGRAMAS = pd.unique(df['Programa Académico']).tolist()

# Dataframe de estudiantes
df_estudiantes = df.iloc[:,25:33]

# Numero total de personas incritas en 2016
TOTAL_INSCRITOS_2016 = sumarInscritos(df_estudiantes)
print("Total de inscritos en 2016: \n", TOTAL_INSCRITOS_2016)

# #
# # Aplicación de filtros
# #

# inscritos por departamento
INSCRITOS_X_DEPARTAMENTOS = [ sumarInscritos( filtarDepartamento(df_estudiantes,DEPARTAMENTOS[i])) for i in range( len(DEPARTAMENTOS) ) ]
# inscritos por municipio
INSCRITOS_X_MUNICIPIOS = [ sumarInscritos( filtarMunicipio( df_estudiantes,MUNICIPIOS[i])) for i in range( len(MUNICIPIOS) ) ]
# programas nacional
PROGRAMAS_X_DEPARTAMENTO = [sumarInscritos(filtrarPrograma(df,PROGRAMAS[i])) for i in range( len(PROGRAMAS))]

# # Filtros por genero

df_Male_Filter = df["Sexo"] == "HOMBRE"
df_Male = df[df_Male_Filter]

df_Female_Filter = df["Sexo"] == "MUJER"
df_Female = df[df_Female_Filter]

# construcción de listas de información
MALE_X_DEPARTAMENTOS = [ sumarInscritos( filtarDepartamento(df_Male,DEPARTAMENTOS[i])) for i in range( len(DEPARTAMENTOS) ) ]
FEMALE_X_DEPARTAMENTOS = [ sumarInscritos( filtarDepartamento(df_Female,DEPARTAMENTOS[i])) for i in range( len(DEPARTAMENTOS) ) ]

MALE_X_MUNICIPIOS = [ sumarInscritos( filtarMunicipio( df_Male,MUNICIPIOS[i])) for i in range( len(MUNICIPIOS) ) ]
FEMALE_X_MUNICIPIOS = [ sumarInscritos( filtarMunicipio( df_Female,MUNICIPIOS[i])) for i in range( len(MUNICIPIOS) ) ]

MALE_X_PROGRAMAS = [sumarInscritos(filtrarPrograma(df_Male,PROGRAMAS[i])) for i in range( len(PROGRAMAS))]
FEMALE_X_PROGRAMAS = [sumarInscritos(filtrarPrograma(df_Female,PROGRAMAS[i])) for i in range( len(PROGRAMAS))]

# Cración del [DataFrame] de información por departamentos.
inscritosDepartamentos = pd.DataFrame( list(zip(DEPARTAMENTOS,MALE_X_DEPARTAMENTOS,FEMALE_X_DEPARTAMENTOS,INSCRITOS_X_DEPARTAMENTOS)), 
                                      columns=["Departamentos","Hombres","Mujeres","Inscritos"])

# Cración del [DataFrame] de información por municipios.
inscritosMunicipio = pd.DataFrame( list(zip(MUNICIPIOS,MALE_X_MUNICIPIOS,FEMALE_X_MUNICIPIOS, INSCRITOS_X_MUNICIPIOS)), 
                                  columns=["Municipios","Hombres","Mujeres", "Inscritos"])

# Cración del [DataFrame] de información por programas.
inscritosProgramas = pd.DataFrame( list(zip(PROGRAMAS,MALE_X_PROGRAMAS,FEMALE_X_PROGRAMAS, PROGRAMAS_X_DEPARTAMENTO)), 
                                  columns=["Programas","Hombres","Mujeres", "Inscritos"])


# # # # # # # # # # # # # #
#      G r á f i c a s    #
# # # # # # # # # # # # # #

# #
# # Preparando la información para realiazar la gráfica No. 2 y 3
# #

# # Operaciones en bloque para obtener promedios  
inscritosDepartamentos["Porcentaje_inscritos"] = ((inscritosDepartamentos["Inscritos"]/TOTAL_INSCRITOS_2016)*100)
inscritosDepartamentos["Porcentaje_hombres"] = ((inscritosDepartamentos["Hombres"]/inscritosDepartamentos["Inscritos"])*100)
inscritosDepartamentos["Porcentaje_mujeres"] = ((inscritosDepartamentos["Mujeres"]/inscritosDepartamentos["Inscritos"])*100)

inscritosMunicipio["Porcentaje_inscritos"] = (inscritosMunicipio["Inscritos"]/TOTAL_INSCRITOS_2016)*100
inscritosMunicipio["Porcentaje_hombres"] = (inscritosMunicipio["Hombres"]/inscritosMunicipio["Inscritos"])*100
inscritosMunicipio["Porcentaje_mujeres"] = (inscritosMunicipio["Mujeres"]/inscritosMunicipio["Inscritos"])*100

inscritosProgramas["Porcentaje_inscritos"] = (inscritosProgramas["Inscritos"]/TOTAL_INSCRITOS_2016)*100
inscritosProgramas["Porcentaje_hombres"] = (inscritosProgramas["Hombres"]/inscritosProgramas["Inscritos"])*100
inscritosProgramas["Porcentaje_mujeres"] = (inscritosProgramas["Mujeres"]/inscritosProgramas["Inscritos"])*100

# Selección de columnas 
grafica_municipios2 = inscritosMunicipio[["Municipios","Porcentaje_hombres","Porcentaje_mujeres"]]
# Dando formato a los números para una mejor presentación
grafica_municipios2['Porcentaje_hombres'] = pd.Series([round(val,2) for val in grafica_municipios2["Porcentaje_hombres"]])
grafica_municipios2['Porcentaje_mujeres'] = pd.Series([round(val,2) for val in grafica_municipios2["Porcentaje_mujeres"]])
# filtro por ciudad
bog = grafica_municipios2["Municipios"] == "Bogota"
med = grafica_municipios2["Municipios"] == "Medellín"
cali = grafica_municipios2["Municipios"] == "Cali"
pal = grafica_municipios2["Municipios"] == "Palmira"
# de dataframe a listas
Bogota = grafica_municipios2[bog].values.tolist()
Medellin = grafica_municipios2[med].values.tolist()
Cali = grafica_municipios2[cali].values.tolist()
Palmira = grafica_municipios2[pal].values.tolist()

gene_Bogota = Bogota[0]
gene_Medellin = Medellin[0]
gene_Cali = Cali[0]
gene_Palmira = Palmira[0]

# grafica_municipios2 = inscritosMunicipio[["Municipios","Porcentaje_hombres","Porcentaje_mujeres"]]

# Gráfica 1--------------------
grafica_municipios1 = inscritosDepartamentos[["Departamentos","Inscritos","Hombres","Mujeres"]]
fig1 = px.bar(grafica_municipios1, x="Departamentos", y=["Hombres","Mujeres"], title="Inscritos por Departamento")
fig1.update_layout(barmode='stack')
fig1.show()
fig1.write_html('figure_1.html', auto_open=True)

# Gráfica 2 -------------------
fig2 = make_subplots(rows=2,cols=2, 
                     specs=[[{"type": "pie"}, {"type": "pie"}],[{"type": "pie"}, {"type": "pie"}]],
                     subplot_titles=("Plot 1","Plot 2","Plot 3","Plot 4"))
fig2.add_trace(go.Pie(values= gene_Bogota[1:3],labels=["Hombres","Mujeres"] ), row=1,col=1)
fig2.add_trace(go.Pie(values= gene_Medellin[1:3],labels=["Hombres","Mujeres"] ), row=2,col=1)
fig2.add_trace(go.Pie(values= gene_Cali[1:3],labels=["Hombres","Mujeres"] ), row=1,col=2)
fig2.add_trace(go.Pie(values= gene_Palmira[1:3],labels=["Hombres","Mujeres"] ), row=2,col=2)
fig2.update_layout(height=700, width=700, title="Porcentajes de inscritos por género en ciudades importantes")
names = {'Plot 1':'Bogotá', 'Plot 2':'Medellín', 'Plot 3':'Cali', 'Plot 4':'Palmira'}
fig2.for_each_annotation(lambda a: a.update(text = a.text + ': ' + names[a.text]))
fig2.update_layout(barmode='stack')
fig2.show()
fig2.write_html('figure_2.html', auto_open=True)

# Gráfica 3 -------------------
fig3 = go.Figure(data=[go.Table(header=dict(values=list(grafica_municipios2.columns),
                                            fill_color='paleturquoise',
                                            align='left'),
                                cells=dict(values=[grafica_municipios2.Municipios, grafica_municipios2.Porcentaje_hombres,grafica_municipios2.Porcentaje_mujeres],
                                          fill_color='lavender',
                                          align='left'))
                                          ])
fig3.update_layout(height=700, width=600, title="Inscritos por género por municipios [%]")
fig3.show()
fig3.write_html('figure_3.html', auto_open=True)


# #
# #  Preparando la información para realiazar la gráfica No. 4
# #
programasOrdenados = inscritosProgramas.sort_values(by='Inscritos', ascending=False)

programas_10 = programasOrdenados.head(10)
programas_antes_lista = programas_10.Programas.values.tolist()
Hombres_antes_lista = programas_10.Hombres.values.tolist()
Mujeres_antes_lista = programas_10.Mujeres.values.tolist()

lista_programas = programas_antes_lista
lista_hombres = Hombres_antes_lista
lista_mujeres = Mujeres_antes_lista

# Gráfica 4 -------------------
fig4 =  go.Figure()
fig4.add_trace(go.Bar(
    y=lista_programas,
    x=lista_hombres,
    name='Hombres',
    orientation='h',
    marker=dict(
        color='rgba(10, 10, 240, 0.6)',
        line=dict(color='rgba(10, 10, 140, 1.0)', width=2)
    )
))
fig4.add_trace(go.Bar(
    y=lista_programas,
    x=lista_mujeres,
    name='Mujeres',
    orientation='h',
    marker=dict(
        color='rgba(240, 10, 10, 0.6)',
        line=dict(color='rgba(240, 10, 10, 1.0)', width=2)
    )
))
fig4.update_layout(height=900, width=700, yaxis_categoryorder = 'total ascending', title="Los 10 programas académicos más inscritos (H vs. M)")
fig4.update_layout(barmode='stack')
fig4.show()
fig4.write_html('figure_4.html', auto_open=True)

# #
# # FIN
# #