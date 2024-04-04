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
from datetime import datetime
# Funciones importadas de funciones_df_crip_tc.py
from funciones_df_crip_tc import get_date,request_coin,get_crip,create_df_crip,web_scraping_tp,enviar_msj_wsp
# Para el manejo de array
import numpy as np
# Librerías necesarias de Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# KEY de la API de Coin
api_key_coin = API_KEY
# Fech actual
input_date= get_date()
# Solicitud de la API
response = request_coin(api_key_coin)

# Recorrer los valores de las criptomonedas
datos = []
for i in tqdm(range(len(response)), colour='blue'):
    datos.append(get_crip(response, i))

# Crear DF
df_crip_top = create_df_crip(datos)
df_tp = web_scraping_tp()

# Enviar mensaje de WSP
mensaje = enviar_msj_wsp(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,df_crip_top,df_tp)

print('Mensaje Enviado con exito ' + mensaje)