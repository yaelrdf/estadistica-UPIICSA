import pandas as pd
import math
import statistics
import matplotlib.pyplot as plt
import nicegui
from nicegui import ui

#Other locals
import operaciones
import renderer

#Global variables to store data between pages
data_gui = None
intervalos_switch = None
calculated_data = {}
amplitud_input = None

##Web user interface
##Main GUI  
def data_capture():
    global data_gui, intervalos_switch
    #Mensaje inicial
    ui.label('Captura de datos').props('header').classes('header')
    ui.restructured_text('Introduzca los valores separandolos por espacios **NO UTILICE SALTOS DE LINEA O COMAS**').classes('center')
    #Espacio de captura
    data_gui = ui.textarea(label='Introduzca los datos').classes('capture').props('clearable')
    #Switch por intervalos
    intervalos_switch = ui.switch('Calcular por intervalos', value=True).props('inline color=green').style('margin: 10px; margin-left: 40px')
    #Boton calculo
    ui.button('Calcular', on_click=lambda: calculate_and_navigate()).classes('button').props('inline color=green')

def calculate_and_navigate():
    global calculated_data
    if data_gui and data_gui.value:
        try:
            # Convert string data to numbers
            data = [float(x) for x in data_gui.value.split()]
            intervalos = intervalos_switch.value if intervalos_switch else False
            
            # Perform calculations
            calculated_data = calculus(data, intervalos)
            ui.navigate.to('/resultados')
        except ValueError:
            ui.notify('Error: Por favor ingrese solo números separados por espacios', type='negative')
    else:
        ui.notify('Error: Ingrese datos para calcular', type='negative')

def recalculate_with_custom_amplitud():
    global calculated_data, amplitud_input
    if amplitud_input and amplitud_input.value:
        try:
            custom_amplitud = float(amplitud_input.value)
            if custom_amplitud <= 0:
                ui.notify('Error: La amplitud debe ser mayor que 0', type='negative')
                return
            
            # Recalculate with custom amplitud
            data = calculated_data['data']
            intervalos = calculated_data['intervalos']
            
            # Perform calculations with custom amplitud
            calculated_data = calculus_with_custom_amplitud(data, intervalos, custom_amplitud)
            
            # Refresh the page to show updated results
            ui.navigate.to('/resultados')
        except ValueError:
            ui.notify('Error: Por favor ingrese un valor numérico válido para la amplitud', type='negative')
    else:
        ui.notify('Error: Ingrese un valor para la amplitud', type='negative')

#Graficadoras
def grapher_acum(df):
    graph_frecuencia = df['Frecuencia absoluta'].tolist()
    graph_medio = df['Punto medio del intervalo'].tolist()
    
    plt.clf()  # Clear previous plot
    plt.title("Histograma")
    plt.xlabel("Punto medio de intervalo")
    plt.ylabel("Frecuencia")
    plt.bar(graph_medio, graph_frecuencia, width=0.5, align='edge')
    plt.grid(axis='y')
        
def grapher_static(df):
    graph_frecuencia = df['Frecuencia absoluta'].tolist()
    graph_medio = df['K'].tolist()
    
    plt.clf()  # Clear previous plot
    plt.title("Histograma")
    plt.xlabel("Clase")
    plt.ylabel("Frecuencia")
    plt.bar(graph_medio, graph_frecuencia, width=1)
    plt.grid(axis='y')

#Funcion Calculo principal
def calculus(data, intervalos):
    n = len(data)
    avg = statistics.mean(data)
    mediana = statistics.median(data)
    try:
        moda = statistics.mode(data)
    except statistics.StatisticsError:
        moda = "No exixte moda unica"
    
    max_val = max(data)
    min_val = min(data)
    
    result = {
        'n': n,
        'avg': avg,
        'mediana': mediana,
        'moda': moda,
        'max_val': max_val,
        'min_val': min_val,
        'intervalos': intervalos,
        'data': data
    }
    
    #Condicional intervalos
    if intervalos:
        #Datos extras
        rango = operaciones.rango(data)
        sturges = operaciones.sturges(data)
        amplitud = operaciones.amplitud(rango, sturges)
        
        tabla = {
            'K': [],
            'Intervalo inferior': [],
            'Intervalo superior': [],
            'Frecuencia absoluta': [],
            'Punto medio del intervalo': [],
            'Frecuencia acumulada': []
        }
        
        #DataFrame
        df = pd.DataFrame(tabla)
        operaciones.filler(df, data, amplitud, min_val, max_val)
        
        result.update({
            'rango': rango,
            'sturges': sturges,
            'amplitud': amplitud,
            'df': df
        })
    else:
        tabla = {
            'K': [],
            'Frecuencia absoluta': [],
            'Frecuencia acumulada': []
        }
        #DataFrame
        df = pd.DataFrame(tabla)
        operaciones.filler_static(df, data)
        result['df'] = df
    
    return result

def calculus_with_custom_amplitud(data, intervalos, custom_amplitud):
    n = len(data)
    avg = statistics.mean(data)
    mediana = statistics.median(data)
    try:
        moda = statistics.mode(data)
    except statistics.StatisticsError:
        moda = "No exixte moda unica"
    
    max_val = max(data)
    min_val = min(data)
    
    result = {
        'n': n,
        'avg': avg,
        'mediana': mediana,
        'moda': moda,
        'max_val': max_val,
        'min_val': min_val,
        'intervalos': intervalos,
        'data': data
    }
    
    #Condicional intervalos
    if intervalos:
        #Datos extras
        rango = operaciones.rango(data)
        sturges = operaciones.sturges(data)
        amplitud = custom_amplitud  # Use custom amplitud instead of calculated one
        
        tabla = {
            'K': [],
            'Intervalo inferior': [],
            'Intervalo superior': [],
            'Frecuencia absoluta': [],
            'Punto medio del intervalo': [],
            'Frecuencia acumulada': []
        }
        
        #DataFrame
        df = pd.DataFrame(tabla)
        operaciones.filler(df, data, amplitud, min_val, max_val)
        
        result.update({
            'rango': rango,
            'sturges': sturges,
            'amplitud': amplitud,
            'df': df
        })
    else:
        tabla = {
            'K': [],
            'Frecuencia absoluta': [],
            'Frecuencia acumulada': []
        }
        #DataFrame
        df = pd.DataFrame(tabla)
        operaciones.filler_static(df, data)
        result['df'] = df
    
    return result

#WEBUI
@ui.page('/')
def main_page():
    ui.page_title('Calculadora Medidas de tendencia central')
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
    renderer.header()
    data_capture()

##Show calculos
@ui.page('/resultados')
def show_data():
    global calculated_data, amplitud_input
    
    if not calculated_data:
        ui.label('No se han ingresado datos').classes('center')
        ui.button('Ingresar datos', on_click=lambda: ui.navigate.to('/')).classes('button')
        return
    
    ui.page_title('Calculadora Medidas de tendencia central')
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
    renderer.header()
    
    #Data things
    ui.label('Datos Utilizados').props('header').classes('header')
    ui.label(str(calculated_data['data'])).classes('center')
    ui.separator()
    
    with ui.grid(columns=2):
        ui.table.from_pandas(calculated_data['df']).classes('center')
        
        #Datos label
        with ui.list().props('separator').style('margin: 0px'):
            ui.item_label('Calculos').props('header').classes('text-bold')
            ui.separator()
            ui.item('Numero de elementos: ' + str(calculated_data['n']))
            ui.item('Valor maximo: ' + str(calculated_data['max_val']))
            ui.item('Valor minimo: ' + str(calculated_data['min_val']))
            ui.item('Media: ' + str(round(calculated_data['avg'], 2)))
            ui.item('Mediana: ' + str(calculated_data['mediana']))
            ui.item('Moda: ' + str(calculated_data['moda']))
            
            #Calculo por intervalos
            if calculated_data['intervalos']:
                ui.item('Rango: ' + str(calculated_data['rango']))
                ui.item('Regla de sturges: ' + str(calculated_data['sturges']))
                ui.item('Amplitud: ' + str(calculated_data['amplitud']))
                
                # Custom amplitud input field and recalculate button
                ui.separator()
                amplitud_input = ui.number('Modificar amplitud:', value=calculated_data['amplitud'], format='%.2f').style('margin: 10px 0')
                ui.button('Recalcular', on_click=recalculate_with_custom_amplitud).classes('button').props('color=blue').style('margin: 5px 0')

        
    with ui.pyplot(figsize=(18, 4)) as plot:
        if calculated_data['intervalos']:
            grapher_acum(calculated_data['df'])
        else:
            grapher_static(calculated_data['df'])
    
ui.run()