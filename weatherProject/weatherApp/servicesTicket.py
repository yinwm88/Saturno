import csv
import json


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
    Función para, dado el ticket, devolver las coordenadas de cada ciudad.
'''
def get_coordenadas_ds(ticket, diccionario): 
    bool = es_ticket(diccionario,ticket)
    if bool:
        clave = ticket
        if diccionario and isinstance(diccionario, dict) and  'origin_latitude' in diccionario[clave] and 'origin_longitude'  in diccionario[clave] and 'destination_latitude' in diccionario[clave] and 'destination_longitude' in diccionario[clave]:
            latO = diccionario[clave]['origin_latitude']
            lonO = diccionario[clave]['origin_longitude']
            latD = diccionario[clave]['destination_latitude']
            lonD = diccionario[clave]['destination_longitude']
            return latO, lonO, latD, lonD
        else:
            return ticket, "si es ticket pero algo anda al con acceder a", None, None
    return ticket,  ticket+ " " + "No es un ticket en:\n" + json.dumps(diccionario), None, None

'''
    Función para obtener los nombres de las ciudades involucradas en el ticket
'''
def get_nombres( ticket, diccionario):
    clave = ticket
     
    cityO = diccionario[clave]['origin']
    cityD = diccionario[clave]['destination']
     
    return cityO, cityD

