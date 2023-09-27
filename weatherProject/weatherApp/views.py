from django.shortcuts import render
import requests
from .servicesTicket import read_data, csv_a_diccionario, es_ticket,  get_coordenadas_ds, get_nombres 

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
    Función para obtener el clima de una ciudad.
'''
def obtener_clima(lat, lon, appid):
    try:
        owUrl = "https://api.openweathermap.org/data/2.5/weather"
        owParams = {'lat': lat, 'lon': lon, 'appid': appid}
        owResp = requests.get(url=owUrl, params=owParams, timeout=20)
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
    Función para mostrar la página de inicio.
'''
def index(request):
    entrada = None
    if request.method == 'POST':
        entrada = request.POST.get('city', '')#puede ser un ticket o nombre
        if entrada:
            appid = read_data('weatherApp/data/apiKey.txt')
            diccionario = csv_a_diccionario('weatherApp/data/dataset2.csv')
            is_ticket = es_ticket(diccionario, entrada)
            if is_ticket:
                ticket = entrada
                entrada = None
                latO, lonO, latD, lonD = get_coordenadas_ds(ticket, diccionario)
                description, icon = obtener_clima(latO, lonO, appid)
                descriptionD, iconD = obtener_clima(latD, lonD, appid)
                cityO, cityD = get_nombres(ticket, diccionario)
                return render(request, 'weatherApp/index.html', {'cityO': cityO,
                                                                 'description': description, 
                                                                 'icon': icon,
                                                                 'cityD':cityD,
                                                                 'descriptionD': descriptionD,
                                                                 'iconD': iconD})
            else:
                city = entrada
                entrada = None
                lat, lon = get_coordenadas_gc(city, appid)
                description, icon = obtener_clima(lat, lon, appid)
                return render(request, 'weatherApp/index.html', {'city':city,
                                                                 'description':description,
                                                                 'icon':icon})                
        else:
            error_message = "Fallo con la entrada"
            return render(request, 'weatherApp/index.html', {'entrada': entrada, 'error_message': error_message})
    return render(request, 'weatherApp/index.html', {'entrada': entrada})
