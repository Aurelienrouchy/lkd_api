from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from pymongo import MongoClient

import time
import unicodedata
import json

from client import ClientManager

client = ClientManager()
client.setup()

mongoClient = MongoClient("mongodb+srv://aurelien:Prout123.!@cluster0.jylje.mongodb.net/lkd?retryWrites=true&w=majority")
db_lkd = mongoClient['lkd']


Peoples = db_lkd['peoples']
Companies = db_lkd['companies']
print(Peoples)
print(Companies)

class Search:

    def __init__(self):
        self.driver = client.driver
        self.history_stack = []

    def start_capture(self):
        client.start_capture()

    def send_to_db_or_save_locally(self, name):
        time.sleep(5)
        har_parsed = self.parse_and_format_har(client.client.har)
        company = {}

        if len(har_parsed) != 0:
            if "companyUrn" in har_parsed[0]:
                company["_id"] = har_parsed[0]["companyUrn"]
            elif "companyName" in har_parsed[0]:
                company["_id"] = har_parsed[0]["companyName"]
            else:
                company["_id"] = name
            
            if "companyName" in har_parsed[0]:
                company["name"] = har_parsed[0]["companyName"]
            else:
                company["name"] = self.driver.current_url

            if "companyUrn" in har_parsed[0]:
                company["companyUrn"] = har_parsed[0]["companyUrn"]

            try:
                Companies.update({"_id": company["_id"]}, company, upsert=True)
        
                for i in range(len(har_parsed)):
                    Peoples.update({"_id": har_parsed[i]["_id"]}, har_parsed[i], upsert=True)
            
            except:
                company["people"] = har_parsed

                with open(f'{company["name"]}_{company["companyUrn"]}.txt', 'w') as text_file:
                    json.dump(company, text_file)
                
        else:
            self.add_one_page_company_for_later()

    def parse_and_format_har(self, har):
        entries = har['log']['entries']
        new_har = []
        for entrie in entries:
            if "https://www.linkedin.com/sales-api/salesApiPeopleSearch" in entrie['request']['url']:
                
                if entrie["response"]["content"]["text"]:
                    text = entrie["response"]["content"]["text"]

                    json_text = json.loads(text)
                    elements = json_text["elements"]

                    for element in elements:
                        obj = {}
                        if "objectUrn" in element:
                            obj["_id"] = element["objectUrn"]
                        if element["firstName"]:
                            obj["firstName"] = element["firstName"]
                        if element["lastName"]:
                            obj["lastName"] = element["lastName"]

                        for pos in element["currentPositions"]:
                            if "companyName" in pos:
                                obj["companyName"] = pos["companyName"]
                            if "companyUrn" in pos:
                                obj["companyUrn"] = pos["companyUrn"]
                            if "current" in pos:
                                obj["current"] = pos["current"]
                            if "title" in pos:
                                obj["title"] = pos["title"]
                            if "startedOn" in pos and 'year' in pos['startedOn'] and 'month' in pos['startedOn']:
                                obj["startedOn"] = f"{pos['startedOn']['month']} {pos['startedOn']['year']}"

                        new_har.append(obj)

        return new_har

    def authenticate(self, username, password):
        self.driver.get("https://www.linkedin.com/uas/login?session_redirect=%2Fsales&fromSignIn=true&trk=navigator")
        
        username_input = self.wait_by("id", "username")
        username_input.send_keys(username)
        
        password_input = self.wait_by("id", "password")
        password_input.send_keys(password + Keys.ENTER)

    def open_company_search(self):
        self.driver.get("https://www.linkedin.com/sales/search/company")
    
    def open_people_search(self):
        self.driver.get("https://www.linkedin.com/sales/search/people")

    def search_by(self, value, button_label, placeholder_value):
        # Search, wait and click on the expand button
        location_button = self.wait_by("xpath", f"//*[@aria-label='{button_label}']")
        location_button.click()
        # Search, wait and add value in the input
        if placeholder_value:
            search_bar = self.wait_by("xpath", f"//*[@placeholder='{placeholder_value}']")
            search_bar.send_keys(value + Keys.ENTER)
        # Search, wait and click on the searched value
        location_found = self.wait_by("xpath", f"//*[@title='{value}']")
        location_found.click()

    def serch_by_secteur(self, secteur):
        self.search_by(secteur, "Agrandir pour modifier le filtre Secteur", "Ajouter des secteurs d’activité")

    def serch_by_location(self, location):
        self.search_by(location, "Agrandir pour modifier le filtre Zone géographique", "Ajouter des lieux")

    def serch_by_size(self, size):
        # Search, wait and click on the expand button
        size_button = self.wait_by("xpath", "//*[@aria-label='Agrandir pour modifier le filtre Effectifs de l’entreprise']")
        size_button.click()
        # Search, wait and click on the searched value
        
        self.wait_by("class_name", "search-filter-typeahead__suggestion-item-value")
        elems_comparaison = {}
        elems = self.driver.find_elements(By.CLASS_NAME, "search-filter-typeahead__suggestion-item-value")
        elems_comparaison["Indépendant"] = elems[0]
        elems_comparaison["1-10"] = elems[1]
        elems_comparaison["11-50"] = elems[2]
        elems_comparaison["51-200"] = elems[3]
        elems_comparaison["201-500"] = elems[4]
        elems_comparaison["501-1 000"] = elems[5]
        elems_comparaison["1 001-5 000"] = elems[6]
        elems_comparaison["5 001-10 000"] = elems[7]
        elems_comparaison["+ de 10 000"] = elems[8]

        elems_comparaison[size].click()

    def search_employes_link(self):
        self.wait_by("class_name", "result-context__entry-points")
        self.scroll_dowm()
        elems = self.driver.find_elements(By.CLASS_NAME, "result-context__entry-points")
        return [elem.get_attribute('href') for elem in elems] 

    def scroll_dowm(self):
        height = self.driver.execute_script("return document.body.scrollHeight;")
        step = height / 5

        for i in range(5):
            self.driver.execute_script(f"window.scrollTo({i * step}, {(i + 1) * step});")
            time.sleep(0.2)

    def open_tab(self, link):
        # Save original tab
        original_tab = self.driver.current_window_handle
        # Add original tab to history
        if original_tab not in self.history_stack:
            self.history_stack.append(original_tab)
        # Open link in new tab with JS 
        self.driver.execute_script(f"window.open( '{link}' ,'_blank');")
        # Search new tab and switch to this one
        for window_handle in self.driver.window_handles:
            if window_handle not in self.history_stack:
                self.driver.switch_to.window(window_handle)
                self.history_stack.append(original_tab)
                self.start_capture()
                break
        
    def close_tab(self):
        #Close the tab or window
        self.driver.close()
        #Switch back to the old tab or window
        self.driver.switch_to.window(self.history_stack[-1])

    def add_one_page_company_for_later(self):
        cssCompanyName = self.wait_by("class_name", "Sans-16px-black-60%-bold-open ember-view")
        companyName = None

        if cssCompanyName:
            companyName = cssCompanyName
        else:
            companyName = self.driver.current_url

        with open("companies_name_one_page.txt", "a+") as text_file:
            # Move read cursor to the start of file.
            text_file.seek(0)
            # If file is not empty then append '\n'
            data = text_file.read(100)
            if len(data) > 0 :
                text_file.write("\n")
            # Append companyName at the end of file
            text_file.write(companyName)
        
    def scroll_and_go_last_page(self, page_name):
        is_end = False
        no_result = self.wait_by("class_name", "search-results__no-results")
        
        if no_result:
            self.close_tab()
            return True
        else:
            while is_end == False:
                self.scroll_dowm()
                next_button = self.wait_by("class_name", "search-results__pagination-next-button")
                if next_button:
                    is_disabled = next_button.get_attribute('disabled')

                    if is_disabled == None:
                        next_button.click()
                    else:
                        self.scroll_dowm()
                        page_one_button = self.wait_by("xpath", f"//*[@data-page-number='1']")
                        if page_one_button:
                            page_one_button.click()

                        result = self.wait_by("class_name", "result-lockup__name")
                        if result:
                            self.scroll_dowm()

                        self.send_to_db_or_save_locally(page_name)
                        self.close_tab()
                        is_end = True
                else:
                    time.sleep(1)
                    continue

        return is_end
     
    def scroll_and_go_last_page_companies(self):
        is_end = False
        first_poeple = self.wait_by("class_name", "result-lockup__name")
        companies = []
        
        if first_poeple:
            while is_end == False:
                is_disabled = None
                self.scroll_dowm()
                next_button = self.wait_by("class_name", "search-results__pagination-next-button")
                if next_button:
                    is_disabled = next_button.get_attribute('disabled')
                else:
                    time.sleep(1)
                    self.scroll_dowm()
                    continue
                companies_on_page = self.search_employes_link()
                companies.append(companies_on_page)

                if is_disabled == None:
                    next_button.click()
                else:
                    break
            
        return companies
    
    def wait_by(self, type_of_value, value):
        try:
            if type_of_value == 'xpath':
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, value)))
                return element

            elif type_of_value == 'class_name':
                element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, value)))
                return element 

            elif type_of_value == 'id':
                element = self.wait.until(EC.presence_of_element_located((By.ID, value)))
                return element

            else:
                print("Wait_by: Not a good value")
            
        except:
            print(f"Element with {type_of_value}: {value}, not found")
            return False


        
    @property
    def wait(self):
        return WebDriverWait(self.driver, 3)