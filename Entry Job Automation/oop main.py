import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class Job_entry_bot:
    def __init__(self):
        self.rental_listings_links = []
        self.rental_prices_listings = []
        self.rental_listings_addresses = []
        self.headers = {
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/103.0.0.0 "
                          "Safari/537.36 ",
        }
        self.GOOGLE_FORMS_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSf2JG4DZV8uTzWbC3ML4_AS2HN_NOXrofClhyU43dvYtgmPaQ' \
                                 '/viewform?usp=sf_link '
        self.ZILLOW_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B' \
                          '%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.79725111914063%2C%22east%22%3A-122' \
                          '.06940688085938%2C%22south%22%3A37.348562092693584%2C%22north%22%3A38.19957188396605%7D%2C' \
                          '%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D' \
                          '%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A' \
                          '%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22' \
                          '%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D' \
                          '%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C' \
                          '%22isListVisible%22%3Atrue%7D '
        response = requests.get(url=self.ZILLOW_URL, headers=self.headers)
        zillow_data = response.text
#         chrome_driver_path = 'C:\Development\chromedriver_win32\chromedriver.exe'
#         service = Service(chrome_driver_path)
#         driver = webdriver.Chrome(service=service)
#         driver.get(self.ZILLOW_URL)
#         time.sleep(10)

#         #  Slow scroll to bottom
#         scroll_window = driver.find_element(By.ID, "search-page-list-container")
#         multiplier = 0.1
#         for n in range(10):
#             multiplier_str = str(multiplier)
#             driver.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight * {multiplier_str}",
#                                   scroll_window)
#             multiplier += 0.1
#             time.sleep(3)
        soup = BeautifulSoup(zillow_data, 'html.parser')
        self.soup = BeautifulSoup(zillow_data, 'html.parser')
        self.links = soup.find_all(name="a", class_="list-card-link")
        self.prices = soup.find_all(class_="list-card-price")
        self.addresses = soup.find_all(class_="list-card-addr")

    def link(self):
        for link in self.links:
            if link['href'].startswith('/b'):
                link['href'] = 'https://www.zillow.com' + link['href']
                self.rental_listings_links.append(link['href'])
        print(self.rental_listings_links)

    def price(self):
        for price in self.prices:
            price_text = price.getText()
            strip_price = price_text.strip("/mo+ 1 bd")
            self.rental_prices_listings.append(strip_price)
        print(self.rental_prices_listings)

    def address(self):
        for address in self.addresses:
            address_text = address.getText()
            clean_address = address_text.replace("|", "")
            self.rental_listings_addresses.append(clean_address)
        print(self.rental_listings_addresses)

    def fill_form(self):
        chrome_driver_path = 'C:\Development\chromedriver_win32\chromedriver.exe'
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service)
        driver.get(url=self.GOOGLE_FORMS_LINK)
        for i in range(len(self.rental_listings_links)):
            time.sleep(2)
            print('fjfglf')
            question_1 = driver.find_elements(By.CSS_SELECTOR, "div.Xb9hP input")[0]
            question_1.send_keys(self.rental_listings_addresses[i])

            question_2 = driver.find_elements(By.CSS_SELECTOR, "div.Xb9hP input")[1]
            question_2.send_keys(self.rental_prices_listings[i])

            question_3 = driver.find_elements(By.CSS_SELECTOR, "div.Xb9hP input")[2]
            question_3.send_keys(self.rental_listings_links[i])

            submit = driver.find_element(By.CSS_SELECTOR, "div.lRwqcd div")
            submit.click()

            another_response = driver.find_element(By.LINK_TEXT, 'Submit another response')
            another_response.click()


entry_bot = Job_entry_bot()
entry_bot.link()
entry_bot.price()
entry_bot.address()
entry_bot.fill_form()
