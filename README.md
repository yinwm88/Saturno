<div align="center">

# **⛈Saturno⛈** #

</div>
<div>

  ⛈<b>Saturno</b>⛈ es una aplicación web para consultar el clima de una ciudad dado el nombre de la ciudad, o de dos ciudades dado un ticket; Fue desarrollada con el web framework     de  [Django](https://www.djangoproject.com/).
  
</div>


<div>
  
  # **Propósito**
  
</div>

<div><b>Consultar el clima de una ciudad dado su nombre:</b></div>

Esto se lográ a través de las peticiones realizadas a  [Geocoding](https://openweathermap.org/api/geocoding-api#direct_name) para obtener las coordenadas y luego a [OpenWeather](https://openweathermap.org/current#one) para consultar la descripción del clima.

<div><b>Consultar el clima de la ciudad de origen y la de destino, apartir del número de ticket dado:</b></div>

Esto e lográ a través de consultar el diccionario generado por el archivo.csv dado.


> La consultar en OpenWeather se hará através de las coordenas de la ciudad, ya que, hacer la consulta directamente  por el nombre de la ciudad [ha quedado obsoleto](https://openweathermap.org/current#builtin)

<div>
  
# **Usage**   

</div>
