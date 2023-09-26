
from django.urls import path, include

urlpatterns = [
    path('', include('weatherApp.urls')),
    #cuando alguien acceda al url '' (means example.com for example), con esa direccion va a ir al lugar de weatherApp.urls, o sea que vaya a views y corra index 
]
