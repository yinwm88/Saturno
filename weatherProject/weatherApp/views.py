from django.shortcuts import render
import requests
#responsable to showing the view of the website
#here we can have funtion that render at html page for us

def index(request):
    appid = '763bec3046693d8461d72f2517e2d1c2'
    city = request.POST.get('city', '')  # Utiliza get para obtener el valor de 'city' o una cadena vacía si no está presente.
    icon = None

   #obtener las coordenadas apartir del nombre de la ciudad
    if city:
        URL = f"http://api.openweathermap.org/geo/1.0/direct"
        PARAMS = {'q': city, 'appid': appid}
        
        try:
            ans = requests.get(url=URL, params=PARAMS)
            ans.raise_for_status()  # Lanza una excepción si hay un problema con la solicitud HTTP
            djson = ans.json()
            
            if djson and isinstance(djson, list) and 'lat' in djson[0] and 'lon' in djson[0]:
                lat = djson[0]['lat']
                lon = djson[0]['lon']
                
                URL = f"https://api.openweathermap.org/data/2.5/weather"
                PARAMS  = {'lat':lat, 'lon':lon, 'appid':appid}
    
                ans = requests.get(url=URL, params=PARAMS)
                djson = ans.json()
                weather = djson['weather']
                icon = weather[0]['icon']    
                description = weather[0]['description']
                
            else:
                lat = None
                lon = None          
        except requests.exceptions.RequestException as e: # Manejar errores de solicitud (por ejemplo, problemas de red o de la API)
            lat = None
            lon = None
    else:
        icon = None
        return render(request, 'weatherApp/index.html', {})
        
    if lat is None  and lon is None:
         description = "No disponible"
         icon = None
         
    return render(request, 'weatherApp/index.html', {'city': city, 'description': description, 'icon': icon })

    
    
    
   
    
    
    #esta funcion va a renderizar dos cosas por ahora: va a ser el request y un pagina html   
   #return render(rerquest, 'weatherApp/index.html)
    