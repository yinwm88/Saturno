from django.shortcuts import render
import requests
import csv


'''
    Funcion para leer el contenido de un archivo.txt.
'''
def read_data(rute):
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
    Función para ver si la llave se encuentra en el diccionario, 
    con esto revisaremos si la entrada es un ticket o un nombre de una ciudad
'''
def es_ticket(diccionario, clave):
    if clave in diccionario:
        return True
    else:
        return False




'''
    Funcion para obtener coordenas con GeoCoding.
'''
def get_coordenadas_gc(city, appid):
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
    Función para, dado el ticket, devolver las coordenadas de cada ciudad.
'''
def get_coordenadas_ds(ticket, diccionario): 
    if diccionario  and 'origin_latitude' in diccionario[ticket] and 'origin_longitude'  in diccionario[ticket] and 'destination_latitude' in diccionario[ticket] and 'destination_longitude' in diccionario[ticket]:
        latO = diccionario[ticket]['origin_latitude']
        lonO = diccionario[ticket]['origin_longitude']
        latD = diccionario[ticket]['destination_latitude']
        lonD = diccionario[ticket]['destination_longitude']
        return latO, lonO, latD, lonD
    else:
        return ticket, "No es un ticket.", None, None
    

'''
    Función para obtener el clima de una ciudad.
'''
import requests

def obtener_clima(lat, lon, appid):
    try:
        owUrl = "https://api.openweathermap.org/data/2.5/weather"
        owParams = {'lat': lat, 'lon': lon, 'appid': appid}
        owResp = requests.get(url=owUrl, params=owParams)
        owResp.raise_for_status()
        djsonOW = owResp.json()

        clima = djsonOW['weather'][0]
        icon = clima['icon']
        description = clima['description']
        return description, icon
    except requests.exceptions.RequestException as e:
        # Captura excepciones relacionadas con la solicitud HTTP
        return "Error de solicitud HTTP:", str(e)
    except KeyError as e:
        # Captura excepciones si la estructura JSON no coincide con lo esperado
        return "Error al procesar la respuesta JSON:", str(e)
    except Exception as e:
        # Captura cualquier otra excepción no manejada
        return "Error desconocido:", str(e)

       

'''
    Función para obtener los nombres de las ciudades involucradas en el ticket
'''
def get_nombres( ticket, diccionario):
    clave = ticket
     
    cityO = diccionario[clave]['origin']
    cityD = diccionario[clave]['destination']
     
    return cityO, cityD



'''
    Función para mostrar la página de inicio.
    La entrada puede er un ticket o el nombre de una ciudad
'''
def index(request):
    entrada, description, icon = None, None, None  
    if request.method == 'POST':
        entrada = request.POST.get('city', '')#puede ser un ticket o nombre
        if entrada:
            descriptionD, iconD = None, None
            appid = '7e0007b2bdccf8fd143f738bc8d7644b'
            ticket = entrada
            entrada = None
            diccionario = csv_a_diccionario('data/dataset2.csv')
            latO, lonO, latD, lonD = get_coordenadas_ds(ticket, diccionario)
            description, icon = obtener_clima(latO, lonO ,appid) 
            descriptionD, iconD = obtener_clima(latD, lonD, appid)
            return render(request, 'weatherApp/index.html', {'entrada': entrada, 
                                                            'description': description, 
                                                            'icon': icon,
                                                            'descriptionD': descriptionD,
                                                            'iconD': iconD})
    else:
        error_message = "Fallo con la entrada"
        return render(request, 'weatherApp/index.html', {'entrada': entrada, 'error_message': error_message})
    return render(request, 'weatherApp/index.html', {'entrada': entrada})
