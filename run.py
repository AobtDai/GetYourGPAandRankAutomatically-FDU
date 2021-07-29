from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import time

proxypool_url = 'http://localhost:5555/random'
def get_random_proxy():
    proxy = requests.get(proxypool_url).text.strip()
    proxy = proxy.replace(':','：')
    return proxy

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
proxy = get_random_proxy()
# print(proxy+'\n')
chrome_options.add_argument('--proxy-server=http://' + proxy)
browser = webdriver.Chrome(options=chrome_options)
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400,900)

def getrank(soup):
    students = soup.find(class_ = 'grid').find('tbody').find_all('tr')
    # print(str(students))
    for student in students:
        infor = student.find_all('td')
        if infor[0].string == "":
            print(infor[1].string+'    '+infor[5].string+'    '+infor[7].string+'\n')
            break


if __name__ == "__main__" :
    url = "https://jwfw.fudan.edu.cn/"
    browser.get(url)

    username = WAIT.until(EC.presence_of_element_located(((By.XPATH, '//*[@id="username"]'))))
    username.send_keys('')
    passwd = WAIT.until(EC.presence_of_element_located(((By.XPATH, '//*[@id="password"]'))))
    passwd.send_keys('')
    signin = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idcheckloginbtn"]')))
    signin.click()
    print("Successfully sign in\n")

    time.sleep(1)
    browser.refresh()
    # 刷新掉踢出重复登录的确认页面

    rank = WAIT.until(EC.element_to_be_clickable((By.XPATH,'//*[@href="/eams/myActualGpa.action"]')))
    rank.click()

    WAIT.until(EC.presence_of_element_located(((By.XPATH, '//*[@class="grid"]'))))
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    getrank(soup)
