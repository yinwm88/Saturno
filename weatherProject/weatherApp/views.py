from django.shortcuts import render
import requests

# Función para obtener el clima de una ciudad
def get_weather(city, appid):
    try:
        geoUrl = "http://api.openweathermap.org/geo/1.0/direct"
        geoParams = {'q': city, 'appid': appid}
        geoResp = requests.get(url=geoUrl, params=geoParams)
        geoResp.raise_for_status()
        djsonGC = geoResp.json()

        if djsonGC and isinstance(djsonGC, list) and 'lat' in djsonGC[0] and 'lon' in djsonGC[0]:
            lat = djsonGC[0]['lat']
            lon = djsonGC[0]['lon']

            owUrl = "https://api.openweathermap.org/data/2.5/weather"
            owParams = {'lat': lat, 'lon': lon, 'appid': appid}
            owResp = requests.get(url=owUrl, params=owParams)
            owResp.raise_for_status()
            djsonOW = owResp.json()

            clima = djsonOW['weather'][0]
            icon = clima['icon']
            description = clima['description']
            return city, description, icon
        else:
            return city, "No se encontro lugar..", None
    except requests.exceptions.RequestException as e:
        return city, "No se encontro el clima.", None

# Función para mostrar la página de inicio
def index(request):
    city, description, icon = None, None, None

    if request.method == 'POST':
        city = request.POST.get('city', '')
        if city:
            appid = '763bec3046693d8461d72f2517e2d1c2'
            city, description, icon = get_weather(city, appid)

    return render(request, 'weatherApp/index.html', {'city': city, 'description': description, 'icon': icon })
