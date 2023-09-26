from django.shortcuts import render
import requests
import csv


'''
    Funcion para leer el contenido de un archivo.txt.
'''
def readData(rute):
    with open(rute, 'r') as txt_file:
                content = txt_file.read()
    return content


'''
    Función para convertir archivos.csv a un diccionario.
'''
def csv_a_diccionario(archivo):
    diccionario = {}
    try:
        with open(archivo, mode='r', newline='') as archivo:
            lector_csv = csv.DictReader(archivo)
            
            for fila in lector_csv:
                clave = fila.pop(lector_csv.fieldnames[0])
                diccionario[clave] = fila

    except FileNotFoundError:
        print(f"El archivo '{archivo}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

    return diccionario

'''
    Función para ver si la llave se encuntra en el diccionario, 
    con esto revisaremos si la entrada es un ticket o un nombre de una ciudad
'''
def esTicket(diccionario, clave):
    if clave in diccionario:
        return True
    else:
        return False


'''
    Función para, dado el ticket, ver si existe y, en dado 
    de que el ticket si exista, no devolvera las coordenadas de cada ciudad.
'''

'''
    Funcion para obtener coordenas con GeoCoding.
'''
def getCoordenasGC(city, appid):
    try:
        geoUrl = "http://api.openweathermap.org/geo/1.0/direct"
        geoParams = {'q': city, 'appid': appid}
        geoResp = requests.get(url=geoUrl, params=geoParams)
        geoResp.raise_for_status()
        djsonGC = geoResp.json()
        if djsonGC and isinstance(djsonGC, list) and 'lat' in djsonGC[0] and 'lon' in djsonGC[0]:
            lat = djsonGC[0]['lat']
            lon = djsonGC[0]['lon']
            return lat,lon
        else:
            return city, "No se pudo localizar.", None
    except requests.exceptions.RequestException as e:
        return city, "No se encontro el clima.", None

'''
    Función para obtener el clima de una ciudad.
'''
def obtenerClima(lat, lon, appid):
    owUrl = "https://api.openweathermap.org/data/2.5/weather"
    owParams = {'lat': lat, 'lon': lon, 'appid': appid}
    owResp = requests.get(url=owUrl, params=owParams)
    owResp.raise_for_status()
    djsonOW = owResp.json()

    clima = djsonOW['weather'][0]
    icon = clima['icon']
    description = clima['description']
    return description, icon
       

'''
    Función para obtener los climas de las ciudades involucradas en un ticket de viaje.
'''
def obtenerClimas(func, lat1, lon1, lat2, lon2, appid):
        clima1 = func(lat1, lon1, appid)
        clima2 = func(lat2, lon2, appid) 
        return clima1, clima2

'''
    Función para mostrar la página de inicio.
    La entrada puede er un ticket o el nombre de una ciudad
'''
def index(request):
    entrada, description, icon = None, None, None
    if request.method == 'POST':
        entrada = request.POST.get('city', '')#puede ser un ticket o nombre
        if entrada:
            appid = readData('data/apiKey.txt')
            lat, lon = getCoordenasGC(entrada, appid)
            description, icon = obtenerClima(lat, lon, appid)

    return render(request, 'weatherApp/index.html', {'entrada': entrada, 
                                                     'description': description, 
                                                     'icon': icon })
