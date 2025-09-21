import math
import numpy
import statistics
import pandas

#Datos basicos
def rango(data):
    return max(data)-min(data)

def sturges(data):
    stu=(1+(10/3))*numpy.log10(len(data))
    return math.ceil(stu)
    
def amplitud(rango,sturges):
    a=rango/sturges
    a=math.ceil(a)
    return a

def frecuencia(data, lower_bound, upper_bound):
    return len([x for x in data if lower_bound <= x < upper_bound])

#Data operations
#Filler
def filler(df,data,amp,min,max):
    # 1er Fill
    Intervalo_superior=min+amp
    Intervalo_inferior=min
    Frecuencia=frecuencia(data,Intervalo_inferior,Intervalo_superior)
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
        Frecuencia=frecuencia(data,inferior,superior)
        p_medio=statistics.mean([inferior,superior])
        #Acumulada
        Acumulada=(df.iloc[len(df)-1,5])+Frecuencia
        
        df.loc[len(df)]= [k,inferior,superior,Frecuencia,p_medio,Acumulada]
