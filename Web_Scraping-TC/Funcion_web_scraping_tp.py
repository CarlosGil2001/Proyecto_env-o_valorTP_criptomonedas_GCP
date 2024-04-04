# Para la manipulación de datos
import pandas as pd
# Para el manejo de array
import numpy as np
# Librerías necesarias de Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# SE INCORPORARÁ AL ARCHIVO DE ENVIO DE MENSAJE EN TWILIO

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
    df_tp = pd.DataFrame(data, columns=['Moneda', 'Compra', 'Estado_Compra', 'Venta','Estado_Venta'])
    return df_tp