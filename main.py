import pandas
import math
import statistics
import operaciones
import matplotlib.pyplot as plt

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
#Reciclados
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

df=pandas.DataFrame(tabla)

#Filler
def filler(dataset,data,amp):
    # 1er Fill
    Intervalo_superior=min+amp
    Intervalo_inferior=min
    Frecuencia=operaciones.frecuencia(data,Intervalo_inferior,Intervalo_superior)
    Punto_medio=statistics.mean([Intervalo_inferior,Intervalo_superior])
    Acumulada=Frecuencia
    
    df.loc[len(df)]= [1,Intervalo_inferior,Intervalo_superior,Frecuencia,Punto_medio,Acumulada]
    
    k=1
    #Fill consequent
    while (df.iloc[len(df)-1,2]) <= max :
        k=k+1
        inferior=(df.iloc[len(df)-1,2])
        superior=(df.iloc[len(df)-1,2])+amp
        #Frecuencias
        Frecuencia=operaciones.frecuencia(data,inferior,superior)
        p_medio=statistics.mean([inferior,superior])
        #Acumulada
        Acumulada=(df.iloc[len(df)-1,5])+Frecuencia
        
        df.loc[len(df)]= [k,inferior,superior,Frecuencia,p_medio,Acumulada]
    
def grapher(df):
    graph_frecuencia= df['Frecuencia absoluta'].tolist()
    graph_medio=df['Punto medio del intervalo'].tolist()
    
    plt.title("Histograma")
    plt.xlabel("Punto medio de intervalo")
    plt.ylabel("Frecuencia")
    plt.bar(graph_medio,graph_frecuencia)
    #Back grid
    plt.grid(axis='y')
    plt.show()
    
    
#Tester
filler(df,data,amplitud)
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

grapher(df)