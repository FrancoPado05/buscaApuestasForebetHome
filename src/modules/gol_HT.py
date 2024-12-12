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

def buscarPartidosGolHT(dia):
    if dia == 'today':
        url = "https://www.forebet.com/es/predicciones-para-manana/predicciones-1x2"
    elif dia == 'tomorrow':
        url = "https://www.forebet.com/es/predicciones-para-manana/predicciones-1x2"

    
    testeosDeComando(dia)

    driver, tocoBotonMas = abrirPagina(url)

    buscarPartidos(driver, tocoBotonMas)

    driver.quit()

    print('ANALISIS FINALIZADO')

# Funciones modificadas

def condicionesCumplirGenerales(seleccion, partidoParticular):
    if seleccion <= 3:
        return False
    
    league = WebDriverWait(partidoParticular, 20).until(
        EC.presence_of_element_located((By.XPATH, ".//div/div/span[@class = 'shortTag']"))
    )
    if league.text in open("../../assets/files/not_interested_leagues.txt").read():
        return False
    
    return True

# Resto de funciones
def testeosDeComando(argumento):
    if argumento not in ['today', 'tomorrow']:
        sys.exit('today, tomorrow')

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
    elements = WebDriverWait(webpage_driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, '//span[text()="Más"]'))
    )

    for mas in elements:
        element = mas

    pinParaMoverse = WebDriverWait(webpage_driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='f-slog']"))
    )

    # Desplázate hasta el elemento
    actions = ActionChains(webpage_driver)
    actions.move_to_element(pinParaMoverse).perform()

    # Haz clic en el elemento "Más"
    element.click()

    if elements == 2:
        return True
    
    return False

def partidoCumpleGeneral(partidoParticular):
    try:
        resultado = WebDriverWait(partidoParticular, 20).until(
            EC.presence_of_element_located((By.XPATH, ".//div[@class='ex_sc tabonly']"))
        )
    except:
        return False

    sumaDeGoles = sum(map(lambda x: int(x), resultado.text.split('-')))

    return condicionesCumplirGenerales(sumaDeGoles, partidoParticular)

def abrirPartidosSeleccionados(driverPartidosSeleccionados):
    for driverPartidoSeleccionado in driverPartidosSeleccionados:
        dirty_link = WebDriverWait(driverPartidoSeleccionado, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
        link = dirty_link.get_attribute("href")
        time.sleep(1)
        webbrowser.open(link)

if __name__ == "__main__":
    main()