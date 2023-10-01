from django.shortcuts import render
import requests
from .servicesTicket import read_data, csv_a_diccionario, es_ticket,  get_coordenadas_ds, get_nombres 
from django.conf import settings
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
            return city, "No se pudo localizar."
    except requests.exceptions.RequestException as e:
        return city, "No se encontro el clima."

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
        temp = djsonOW['main']['temp']
        humidity = djsonOW['main']['humidity']
        pressure = djsonOW['main']['pressure']
        wind_speed = djsonOW['wind']['speed']
        icon = clima['icon']
        description = clima['description']
        return temp, humidity, pressure, wind_speed, description, icon  
    
    except requests.exceptions.RequestException as e:
        # Captura excepciones relacionadas con la solicitud HTTP
        return "Error de solicitud HTTP:", str(e), None, None, None, None
    except KeyError as e:
        # Captura excepciones si la estructura JSON no coincide con lo esperado
        return "Error al procesar la respuesta JSON:", str(e), None, None, None, None
    except Exception as e:
        # Captura cualquier otra excepción no manejada
        return "Error desconocido:", str(e), None, None, None, None

       
'''
    Función para mostrar la página de inicio.
'''
def index(request):
    entrada, ticket_input, city_input = None, None, None
    if request.method == 'POST':
        entrada = request.POST.get('city', '')#puede ser un ticket o nombre
        if entrada:
            appid = settings.API_KEY
            diccionario = csv_a_diccionario('weatherApp/data/dataset2.csv')
            is_ticket = es_ticket(diccionario, entrada)
            if is_ticket:
                ticket_input = "Buen viaje! "
                ticket = entrada
                entrada= None
                latO, lonO, latD, lonD = get_coordenadas_ds(ticket, diccionario)
                tempK, humidity, pressure, wind_speed, description, icon = obtener_clima(latO, lonO, appid)
                tempKD, humidityD, pressureD, wind_speedD, descriptionD, iconD = obtener_clima(latD, lonD, appid)
                tempC = round(tempK - 273.15,2)
                tempCD = round(tempKD - 273.15,2)
                cityO, cityD = get_nombres(ticket, diccionario)
                return render(request, 'weatherApp/index.html', {'ticket_input':ticket_input,
                                                                 'cityO': cityO,
                                                                 'tempC':tempC,
                                                                 'humidity':humidity,
                                                                 'pressure':pressure,
                                                                 'wind_speed':wind_speed,
                                                                 'icon': icon,
                                                                 'description': description, 
                                                                 'cityD':cityD,
                                                                 'tempCD':tempCD,
                                                                 'humidityD':humidityD,
                                                                 'pressureD':pressureD,
                                                                 'wind_speedD':wind_speedD,
                                                                 'iconD': iconD,
                                                                 'descriptionD': descriptionD
                                                                 })
            else:
                city_input="Se ingreso una ciudad"
                city = entrada
                entrada, tempC = None, None
                lat, lon = get_coordenadas_gc(city, appid)
                tempK, humidity, pressure, wind_speed, description, icon = obtener_clima(lat, lon, appid)
                tempC = round(tempK - 273.15, 2)
                return render(request, 'weatherApp/index.html', {'city_input': city_input,
                                                                 'city':city,
                                                                 'tempC':tempC,
                                                                 'humidity':humidity,
                                                                 'pressure':pressure,
                                                                 'wind_speed':wind_speed,
                                                                 'description':description,
                                                                 'icon':icon})                
        else:
            error_message = "Fallo con la entrada"
            return render(request, 'weatherApp/index.html', {'entrada': entrada, 'error_message': error_message})
    return render(request, 'weatherApp/index.html', {'entrada': entrada})
