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

def buscarPartidosDeGanador(dia):
        
    url_today = "https://www.forebet.com/es/predicciones-para-hoy/predicciones-1x2"
    url_tomorrow = "https://www.forebet.com/es/predicciones-para-manana/predicciones-1x2"

    if dia.casefold() == "today":
        url = url_today
    elif dia.casefold() == "tomorrow":
        url = url_tomorrow
    else:
        sys.exit("today o tomorrow")

    #service quedo de cuando no usaba seleniumbase para evitar cloudflare
    service = Service(executable_path="chromedriver.exe")
    
    driver = Driver(uc=True)

    driver.get(url)

    clickMoreMatchesButton(driver)

    time.sleep(10)

    entro_a_rcnt_tr_0 = 0

    rcnt_list = ["rcnt tr_1", "rcnt tr_2"]
    
    for _ in range(2):
        if entro_a_rcnt_tr_0 == 0:
            rcnt = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class = 'rcnt tr_0']"))
            )
            counter_to_avoid_match = 0
            for in_rcnt in rcnt:
                if (len(rcnt) - 2) == counter_to_avoid_match:
                    break

                counter_to_avoid_match += 1
                selected_match, status = filterMatch(in_rcnt)
                if selected_match != None:
                    findMatch(selected_match, status)

        elif entro_a_rcnt_tr_0 == 1:
            for search in rcnt_list:
                rcnt = driver.find_elements(By.XPATH, f"//div[@class = '{search}']")
                for in_rcnt in rcnt:
                    selected_match, status = filterMatch(in_rcnt)
                    if selected_match != None:
                        findMatch(selected_match, status)
        entro_a_rcnt_tr_0 = 1

    
    print("ANALISIS FINALIZADO")


def clickMoreMatchesButton(webpage_driver):
    pinParaMoverse = WebDriverWait(webpage_driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='f-slog']"))
    )

    # Desplázate hasta el elemento
    actions = ActionChains(webpage_driver)
    actions.move_to_element(pinParaMoverse).perform()

    try:
        masButton = WebDriverWait(webpage_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mrows"]/span'))
        )
        # Haz clic en el elemento "Más"
        masButton.click()
    except:
        pass

def filterMatch(match_driver):
    league = match_driver.find_element(By.XPATH, ".//div/div/span[@class = 'shortTag']")
    status = -1
    if league.text in open('favourite_leagues.txt').read():
        status = 1
        return match_driver, status
    elif league.text not in open("not_interested_leagues.txt").read():
        status = 0
        return match_driver, status
    else:
        match_driver = None
        return match_driver, status

def findMatch(filtered_match_driver, status):
    forepr = filtered_match_driver.find_element(By.XPATH, ".//div/span[@class = 'forepr']")
    try:
        recent = filtered_match_driver.find_element(By.XPATH, ".//div/span[@class = 'fpr']")
    except NoSuchElementException:
        recent = filtered_match_driver.find_element(By.XPATH, ".//div/span/b")
    home_team = filtered_match_driver.find_element(By.XPATH, ".//div/div/a/span[@class = 'homeTeam']")
    away_team = filtered_match_driver.find_element(By.XPATH, ".//div/div/a/span[@class = 'awayTeam']")
    time = find_time_of_match(filtered_match_driver)
    dirty_link = filtered_match_driver.find_element(By.TAG_NAME, "a")
    link = dirty_link.get_attribute("href")
    if status == 1:
        if forepr.text == "1" or forepr.text == "2":
            abrirLink(100, 50, link, recent.text, time)
    elif status == 0:
        if forepr.text == "1":
            abrirLink(100, 50, link, recent.text, time)

def find_time_of_match(filtered_match_driver):
    match_time = filtered_match_driver.find_element(By.XPATH, ".//div/div/a/span[@class = 'date_bah']")
    _, time = match_time.text.split(" ")
    hours, _ = time.split(":")
    return hours

def abrirLink(top, bottom, link, num, matchTime):
    num = int(num)
    matchTime = int(matchTime)
    if (bottom <= num <= top and (7 <= matchTime <= 23 or 0 <= matchTime <= 1)):
        webbrowser.open(link)
    time.sleep(3)