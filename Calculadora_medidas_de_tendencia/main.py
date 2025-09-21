import pandas as pd
import math
import statistics
import matplotlib.pyplot as plt
import nicegui
from nicegui import ui

#Other locals
import operaciones
import renderer

#Data for testing
data= [49,38,31,27,20,41,33,28,22,48,16,37,31,26,19,41,33,27,21,46,37,45,31,26,18,39,32,27,21,47,37,30,34,25,16,39,31,27,20,45,36,30,24,29,15,44,35,30,24,43,35,29,23,43,23]

#Datos basicos
n=len(data)
avg=statistics.mean(data)
rango=operaciones.rango(data)
sturges=operaciones.sturges(data)
amplitud=operaciones.amplitud(rango,sturges)
mediana=statistics.median(data)
moda=statistics.mode(data)
max=max(data)
min=min(data)

tabla= {
    'K':[],
    'Intervalo inferior':[],
    'Intervalo superior': [],
    'Frecuencia absoluta': [],
    'Punto medio del intervalo':[],
    'Frecuencia acumulada': []
}

df=pd.DataFrame(tabla)

def grapher_acum(df):
    graph_frecuencia= df['Frecuencia absoluta'].tolist()
    graph_medio=df['Punto medio del intervalo'].tolist()
    
    plt.title("Histograma")
    plt.xlabel("Punto medio de intervalo")
    plt.ylabel("Frecuencia")
    plt.bar(graph_medio,graph_frecuencia,width=1)
    #Back grid
    plt.grid(axis='y')
    #plt.show()
    
    
#Tester
operaciones.filler(df,data,amplitud,min,max)

print('N: ',n)
print('Maximo: ',max)
print('Minimo: ',min)
print('Media: ',avg)
print('Mediana: ', mediana)
print('Moda: ', moda)
print('rango: ',rango)
print('Regla de sturges: ', sturges)
print('Amplitud: ',amplitud)

print('\nTabla')
#df=pandas.DataFrame(tabla)
print(df)


#####Web user interface
#Show calculos
def calculo_interval():
    ui.label('Datos Utilizados').props('header').classes('header')
    ui.label(str(data)).classes('center')
    ui.separator()
    with ui.grid(columns=2):
        ui.table.from_pandas(df).classes('center')
        #Datos label
        with ui.list().props('separator').style('margin: 0px'):
            ui.item_label('Calculos').props('header').classes('text-bold')
            ui.separator()
            ui.item('N: '+str(n))
            ui.item('Valor maximo: '+str(max))
            ui.item('Valor minimo: '+str(min))
            ui.item('Media: '+str(round(avg,2)))
            ui.item('Mediana: '+str(mediana))
            ui.item('Moda: '+str(moda))

        with ui.pyplot(figsize=(8, 4)) as plot:
            grapher_acum(df)

def data_capture():
    #Mensaje inicial
    ui.label('Captura de datos').props('header').classes('header')
    ui.restructured_text('Introduzca los valores separandolos por espacios **NO UTILICE SALTOS DE LINEA O COMAS**').classes('center')
    #Espacio de captura
    data_ui=ui.textarea(label='Introduzca los datos').classes('capture').props('clearable')
    #Switch por intervalos
    intervalos = ui.switch('Calcular por intervalos').props('inline color=green').style('margin: 10px; margin-left: 40px')
    #Boton calculo
    ui.button('Calcular', on_click=lambda: ui.notify('You clicked me!')).classes('button').props('inline color=green')
    
##Main GUI  
ui.page_title('Calculadora Medidas de tendendia central')
ui.add_css('''
    .header {
        font-size: 1.75em;
        font-weight: bold;
        margin: auto;
    }
    .center {
        margin: auto;
        text-align: center;
        align-items: center;
    }
    .capture {
        padding: 5px 50px;
        display: flex;
        align-items: center;
        width: 100%;
        margin: 0;
    }
    .button {
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        margin: auto;
        text-align: center;
        align-items: center;
    }
''')


#Header
renderer.index()
#ui.sub_pages({'/':data, '/calculo_intervalos': calculo_interval})
data_capture()
ui.run()