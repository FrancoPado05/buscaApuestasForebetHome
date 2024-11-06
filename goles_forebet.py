import sys
import time
import webbrowser
from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta

def buscarPartidosDeGoles(dia):

    today = datetime.today()
    if dia == 'today':
        url = f'https://www.forebet.com/es/predicciones-de-futbol/predicciones-bajo-mas-2-5-goles/{today.strftime("%Y-%m-%d")}'
    elif dia == 'tomorrow':
        tomorrow = today + timedelta(days=1)
        url = f'https://www.forebet.com/es/predicciones-de-futbol/predicciones-bajo-mas-2-5-goles/{tomorrow.strftime("%Y-%m-%d")}'
    elif dia == 'otro':
        url = input('Poner link aqui: ')

    testeosDeComando(dia)

    driver, tocoBotonMas = abrirPagina(url)

    buscarPartidos(driver, tocoBotonMas)

    driver.quit()

    print('ANALISIS FINALIZADO')

# Funciones 2
def testeosDeComando(dia):
    if dia not in ['today', 'tomorrow', 'otro']:
        sys.exit('today, tomorrow u otro')

def abrirPagina(url):
    driver = Driver(uc=True)

    driver.get(url)

    tocoBotonMas = clickMoreMatchesButton(driver)

    time.sleep(5)

    return driver, tocoBotonMas

def buscarPartidos(driver, tocoBotonMas):
    
    driverPartidosSeleccionados = []
    allRcnt = ['rcnt tr_0', 'rcnt tr_1', 'rcnt tr_2'] if tocoBotonMas else ['rcnt tr_0', 'rcnt tr_1']
    
    for rcnt in allRcnt:
        driverPartidosParticulares = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, f"//div[@class = '{rcnt}']"))
        )
        if rcnt == 'rcnt tr_0':
            del driverPartidosParticulares[-2]
            del driverPartidosParticulares[-1]

        for driverPartidoParticular in driverPartidosParticulares:
            if partidoCumpleGeneral(driverPartidoParticular):
                driverPartidosSeleccionados.append(driverPartidoParticular)
    
    abrirPartidosSeleccionados(driverPartidosSeleccionados)


# Funciones 3
def clickMoreMatchesButton(webpage_driver):

    pinParaMoverse = WebDriverWait(webpage_driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='f-slog']"))
    )


    try:
        masButton = WebDriverWait(webpage_driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mrows"]/span'))
        )
        # Desplázate hasta el elemento
        actions = ActionChains(webpage_driver)
        actions.move_to_element(pinParaMoverse).perform()
        # Haz clic en el elemento "Más"
        masButton.click()
    except:
        print('No toco el boton')
        return False
    
    return True
    
def partidoCumpleGeneral(partidoParticular):
    driverPorbabilidades = WebDriverWait(partidoParticular, 20).until(
        EC.presence_of_element_located((By.XPATH, ".//div[@class='fprc']"))
    )
    
    _, over = encontrarProbabilidades(driverPorbabilidades.text)

    seleccion = over
    
    return condicionesCumplirGenerales(seleccion, partidoParticular)


def abrirPartidosSeleccionados(driverPartidosSeleccionados):
    for driverPartidoSeleccionado in driverPartidosSeleccionados:
        dirty_link = WebDriverWait(driverPartidoSeleccionado, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
        link = dirty_link.get_attribute("href")
        time.sleep(1)
        if chequeoEspecifico(link):
            webbrowser.open(link)


# Funciones 4
def encontrarProbabilidades(driverPorbabilidades):
    under = int(driverPorbabilidades[:2])
    over = int(driverPorbabilidades[2:])

    if under + over == 100:
        return under, over

    if int(driverPorbabilidades[:1]) + int(driverPorbabilidades[1:]) == 100:
        return int(driverPorbabilidades[:1]), int(driverPorbabilidades[1:])

    if int(driverPorbabilidades[:2]) + int(driverPorbabilidades[2:]) == 100:
        return int(driverPorbabilidades[:2]), int(driverPorbabilidades[2:])

    if int(driverPorbabilidades[:3]) == 100:
        return 100, 0

    if int(driverPorbabilidades[3:]) == 100:
        return 0, 100

def condicionesCumplirGenerales(seleccion, partidoParticular):
    if seleccion <= 65:
        return False
    
    match_time = WebDriverWait(partidoParticular, 20).until(
        EC.presence_of_element_located((By.XPATH, ".//div/div/a/span[@class = 'date_bah']"))
    )
    try:
        _, time = match_time.text.split(" ")
    except ValueError:
        return False
    hours, _ = time.split(":")
    if 1 < int(hours) < 7:
        return False
    
    league = WebDriverWait(partidoParticular, 20).until(
        EC.presence_of_element_located((By.XPATH, ".//div/div/span[@class = 'shortTag']"))
    )
    if league.text in open("not_interested_leagues.txt").read():
        return False
    
    return True

def chequeoEspecifico(link):

    service = Service(executable_path="chromedriver.exe")
    driverPartido = webdriver.Chrome(service=service)

    driverPartido.get(link)
    
    tabs = WebDriverWait(driverPartido, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, ".//ul[@class='tabs-ul']/li/a"))
    )

    entro = False

    for tab in tabs:
        if True:
            if tab.text == 'Corners':

                entro = True

                probabilidadesMezcladasCorners = encontrarProbabilidadesEspecificas(tab, driverPartido)
                _, over = probabilidadesMezcladasCorners.split(' ')
                if int(over) < 65:
                    return False
        if tab.text == 'Ambos equipos anotan':
            probabilidadesMezcladasAmbosAnotan = encontrarProbabilidadesEspecificas(tab, driverPartido)
            _, over = encontrarProbabilidades(probabilidadesMezcladasAmbosAnotan)
            condicion = max(int(over), 64) == 64
            if condicion:
                return False
    if not entro:
        return False
    return True

# Funciones 5
def encontrarProbabilidadesEspecificas(tab, driverPartido):
    # Desplázate hasta el elemento
    actions = ActionChains(driverPartido)
    actions.move_to_element(tab).perform()

    tab.click()
    driverPorbabilidades = WebDriverWait(driverPartido, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='rcnt tr_0']/div[@class='fprc']"))
    )

    for d in driverPorbabilidades:
        if d.text != '':
            return d.text