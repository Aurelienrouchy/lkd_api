from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import string

from browsermobproxy import Server
from BmpProxy import ProxyManager
import json
import time
import requests

proxy = ProxyManager()
server = proxy.start_server()
client = proxy.start_client()


options = ChromeOptions()
options.add_argument("--proxy-server={0}".format(client.proxy))


caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

driver = Chrome(options=options, desired_capabilities=caps)
driver.get("https://www.linkedin.com/uas/login?session_redirect=%2Fsales&fromSignIn=true&trk=navigator")

browser_log = driver.get_log('performance') 

username = driver.find_element(By.ID, "username").send_keys("rouchy.aurelien1@gmail.com")
password = driver.find_element(By.ID, "password").send_keys("Odette123" + Keys.ENTER)

wait = WebDriverWait(driver, 10)

# # searchHome = driver.find_element(By.ID, "global-typeahead-search-input").send_keys("" + Keys.ENTER)

# # driver.find_element_by_class_name("search-nav__switch-context search-nav__company-context").click()

driver.get("https://www.linkedin.com/sales/search/people")

# wait.until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Agrandir pour modifier le filtre Titre']")))
# driver.find_element(By.XPATH, "//*[@aria-label='Agrandir pour modifier le filtre Titre']").click()


# input = driver.find_element(By.XPATH, "//*[@placeholder='Ajouter des titres']")

# main_jobs = open("all_jobs.txt", "r")
# print(len(list(main_jobs)))

# arrayText = []
# exist = []
# for word in array_jobs:
#     if word not in exist:

#         exist.append(word)















client.new_har('', options={'captureContent': True})
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Agrandir pour modifier le filtre Secteur']")))
driver.find_element(By.XPATH, "//*[@aria-label='Agrandir pour modifier le filtre Secteur']").click()
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@title='Internet']")))
driver.find_element(By.XPATH, "//*[@title='Internet']").click()
# time.sleep(5)
driver.find_element(By.XPATH, "//*[@aria-label='Agrandir pour modifier le filtre Zone géographique']").click()
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@placeholder='Ajouter des lieux']")))
driver.find_element(By.XPATH, "//*[@placeholder='Ajouter des lieux']").send_keys("Ville de Paris, Île-de-France, France" + Keys.ENTER)
# time.sleep(5)
client.new_har('', options={'captureContent': True})
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@title='Ville de Paris, Île-de-France, France']")))
driver.find_element(By.XPATH, "//*[@title='Ville de Paris, Île-de-France, France']").click()
# time.sleep(5)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "result-context__entry-points")))
# elements = driver.find_elements(By.CLASS_NAME, "result-context__entry-points")
# height = driver.execute_script("return document.body.scrollHeight;")
# step = height / 5

# for i in range(5):
#     driver.execute_script(f"window.scrollTo({i * step}, {(i + 1) * step});")
#     time.sleep(0.2)
# elements[0].click()

# wait.until(EC.presence_of_element_located((By.CLASS_NAME, "result-lockup__name")))
# elementss = driver.find_elements(By.CLASS_NAME, "result-lockup__name")

# elementss[0].click()

with open('./log.har', 'w') as har_file:

# har = client.har
# entries = har['log']['entries']
# arrayText = []

# for entrie in entries:
#     if "https://www.linkedin.com/sales-api/salesApiFacetTypeahead" in entrie['request']['url']:

#         text = entrie['response']['content']['text'].replace('\\"', '"')

#         obj = json.loads(text)
#         jobs = obj['elements']

#         for job in jobs:
#             print(job['displayValue'])
#             arrayText.append(job['displayValue'])

# f.write(str(exist))
    time.sleep(1)
    json.dump(client.har, har_file)




