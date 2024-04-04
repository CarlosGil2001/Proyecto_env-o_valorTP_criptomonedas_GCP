import os
from twilio.rest import Client

# Definimos las configuraciones de CoinAPI y su API
from CoinAPI_key_config import API_KEY
# Definimos las configuraciones para el Twilio API - Mensaje wsp
from twilio_wsp_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,PHONE_NUMBER
# Librería para la hora actual
import time
# Para preparar y enviar solicitudes HHTP
from requests import Request, Session
# Para el manejo de errores
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# Para la codificación y decodificación de JSON
import json
# Para el análisis de datos 
import pandas as pd
# Para enviar solitudes HTTP
import requests
# Para agregar barras de progreso
from tqdm import tqdm
# Para obtener la fecha actual
from datetime import datetime,timedelta
# Para el manejo de array
import numpy as np
# Librerías necesarias de Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


## EXTRAER INFORMACIÓN DE COIN API - CRIPTOMONEDAS

# Funcion que retorna la fecha
def get_date():
    input_date = datetime.now()
    input_date = input_date - timedelta(hours=5) # reducir 5h para adecuar la hora
    input_date = input_date.strftime("%Y-%m-%d %H:%M")
    return input_date


# Función que retorna la solictitud de la API
def request_coin(coin_api_key):
    url_crip = 'https://rest.coinapi.io/v1/assets/apikey-'+ coin_api_key
    try :
        response = requests.get(url_crip).json()
    except Exception as e:
        print(e)
    return response

# Función que recorre y extrae los valores de interés del JSON - API
def get_crip(response, i):
    nombre = response[i]['name']
    precio = response[i].get('price_usd')
    if precio is not None:
        precio = round(precio, 0)
    return nombre, precio

# Función para crear el DF
def create_df_crip(datos):

    # Definimos los nombre de las columnas de DF
    columns = ['Nombre', 'Precio$']
    # Crear el DF
    df_crip = pd.DataFrame(datos,columns=columns)
    df_crip = df_crip.sort_values(by = 'Precio$',ascending = False)
    df_crip

    # Data cleaning
    # Eliminar valores NULL en "Precio$"
    df_crip = df_crip.dropna(subset=['Precio$'])
    # Convertir a tipo de datos INT a "Precio$"
    df_crip['Precio$']=df_crip['Precio$'].astype('int')
    # Filtramos para valores > 0 y < 31000
    df_crip = df_crip.loc[(df_crip['Precio$'] > 0) & (df_crip['Precio$'] <= 31000)]
    # Obtenemos el TOP 5
    df_cript_top=df_crip.head(5)
    
    return df_cript_top


# EXTRAER INFORMACIÓN MEDIANTE WEB SCRAPING - TIPO DE CAMBIO
# Función que configura y obteniene los datos de la Tabla de la pag web de los valores de Tipo de Cambio
def web_scraping_tp():

    # Configuraciones del controlador
    service = Service(executable_path=r'/usr/local/bin/chromedriver') # ruta del controlador en la Compute Engine de GCP
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(service=service, options=options)

    # Ingresando a página web
    browser.get('https://cuantoestaeldolar.pe/')

    # Obtener los datos mediante web scraping
    data = []
    for i in range(1, 5):
        xpath = f'/html/body/div[1]/main/div/div/div[4]/div[1]/div/div/div[2]/div[{i}]'
        text = browser.find_element(By.XPATH, xpath).text
        lines = text.split('\n')
        data.append(lines)

    data = np.array(data).reshape(-1, 5)
    df_tp = pd.DataFrame(data, columns=['Moneda', 'Compra', 'EstComp', 'Venta','EstVent'])
    return df_tp


# ENVIAR MENSAJE 
# Función para mandar el mensaje por WSP
def enviar_msj_wsp(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,df_cript_top,df_tp):

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)
    # Construir el mensaje que se neviará por WSP
    message = client.messages.create(
    from_='whatsapp:'+PHONE_NUMBER,
    body='\nHola!, hoy '  + input_date + '\n\n Los valores de criptomonedas en $ son los siguiente: \n\n'+ str(df_cript_top.to_string(index=False)) + '\n\n Información de los Tipo de Cambio en Perú: \n\n' + str(df_tp.to_string(index=False)),
    to='whatsapp:+51963290272'
    )
    return message.sid
