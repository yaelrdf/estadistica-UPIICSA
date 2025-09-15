import math
import numpy
import statistics
import pandas

#Datos basicos
def media(data):
    return statistics.mean(data)
    
def rango(data):
    return max(data)-min(data)

def sturges(data):
    stu=(1+(10/3))*numpy.log10(len(data))
    return math.ceil(stu)
    
def amplitud(rango,sturges):
    a=rango/sturges
    a=math.ceil(a)
    return a

##Mediana y moda
def moda(data):
    return statistics.mode(data)

def media(data):
    return statistics.median_low(data)
    return statistics.median_high(data)

def frecuencia(data, lower_bound, upper_bound):
    return len([x for x in data if lower_bound <= x < upper_bound])

#TODO
#Subtitute for statistics funtions on actual code.
