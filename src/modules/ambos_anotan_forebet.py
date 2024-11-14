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

if sys.argv[1] == 'today':
    url = 'https://www.forebet.com/es/predicciones-para-hoy/predicciones-bajo-mas-2-5-goles'
elif sys.argv[1] == 'tomorrow':
    url = 'https://www.forebet.com/es/predicciones-para-manana/ambos-equipos-anotaran'
elif sys.argv[1] == 'otro':
    url = input('Poner link aqui: ')

criterio = sys.argv[2]

def main():
    testeosDeComando(sys.argv)

    driver, tocoBotonMas = abrirPagina()

    buscarPartidos(driver, tocoBotonMas)

    driver.quit()

    print('ANALISIS FINALIZADO')

# Funciones modificadas

def chequeoEspecifico(link):

    service = Service(executable_path="C:\Program Files\Google\Chrome\Driver\chromedriver.exe")
    driverPartido = webdriver.Chrome(service=service)

    driverPartido.get(link)
    
    prediccion = WebDriverWait(driverPartido, 20).until(
        EC.presence_of_element_located((By.XPATH, ".//*[@id='m1x2_table']/div[3]/div[4]/span/span"))
    )

    return prediccion.text == 'X'

def condicionesCumplirGenerales(seleccion, partidoParticular):
    if seleccion <= 75:
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

# Resto de funciones
def testeosDeComando(argumentos):
    if len(argumentos) != 3:
        sys.exit('Te faltan o sobran parametros')

    if argumentos[1] not in ['today', 'tomorrow', 'otro']:
        sys.exit('today, tomorrow u otro')

    if argumentos[2] not in ['over', 'under']:
        sys.exit('over o under')

def abrirPagina():
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
    driverPorbabilidades = WebDriverWait(partidoParticular, 20).until(
        EC.presence_of_element_located((By.XPATH, ".//div[@class='fprc']"))
    )
    
    under, over = encontrarProbabilidades(driverPorbabilidades.text)

    seleccion = under if criterio == 'under' else over
    
    return condicionesCumplirGenerales(seleccion, partidoParticular)

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

def abrirPartidosSeleccionados(driverPartidosSeleccionados):
    for driverPartidoSeleccionado in driverPartidosSeleccionados:
        dirty_link = WebDriverWait(driverPartidoSeleccionado, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
        link = dirty_link.get_attribute("href")
        time.sleep(1)
        # if chequeoEspecifico(link):
        webbrowser.open(link)

if __name__ == "__main__":
    main()