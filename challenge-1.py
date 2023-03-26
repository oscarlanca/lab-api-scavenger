# enter your code below
import configparser
import time
import requests
import base64

config = configparser.ConfigParser()
config.read('Ironhack/Config/config2.cfg')

token = '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'
headers = {'Authorization': 'token ' + token}

url_inicial = 'https://api.github.com/repos/ironhack-datalabs/scavenger/contents'

def validar_intentos_restantes(respuesta):
    print('Hora reset',time.ctime(int(respuesta.headers['X-RateLimit-Reset'])))
    print('Intentos restantes',respuesta.headers['X-RateLimit-Remaining'])
    print('Intentos usados',respuesta.headers['X-RateLimit-Used'])
    

def consulta(endpoint, validar_restantes = False, headers = headers):
    response = requests.get(endpoint, headers = headers)
    print(response.status_code)
    if validar_restantes:
        validar_intentos_restantes(response)
    return response.json()

result = consulta(url_inicial)

for directory in result[1:]:
    path_ejemplo = directory['path']
    respuesta_consulta = consulta(f'{url_inicial}/{path_ejemplo}')
    archivos_utiles = [element['path'] for element in respuesta_consulta if element['path'].endswith('hunt')]
    total_archivos += archivos_utiles
    
lista_ordenada = sorted(total_archivos, key = lambda x: x.split('.')[1])

result_file_content = consulta(f'{url_inicial}/{path_ejemplo_file}', True)

coded_string = result_file_content['content']
base64.b64decode(coded_string).decode('utf8')

contenidos = ''
for file in lista_ordenada:
    result_file_content = consulta(f'{url_inicial}/{file}')
    coded_string = result_file_content['content']
    decoded_string = base64.b64decode(coded_string).decode('utf8')
    contenidos += decoded_string

print(contenidos.replace('\n',' '))

