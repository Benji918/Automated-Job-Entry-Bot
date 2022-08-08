import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 "
                  "Safari/537.36 ",
}
GOOGLE_FORMS_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSf2JG4DZV8uTzWbC3ML4_AS2HN_NOXrofClhyU43dvYtgmPaQ' \
                    '/viewform?usp=sf_link '
ZILLOW_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C' \
             '%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A' \
             '-122.17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C' \
             '%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A' \
             '%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse' \
             '%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B' \
             '%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D' \
             '%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min' \
             '%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D '
response = requests.get(url=ZILLOW_URL, headers=headers)
zillow_data = response.text
soup = BeautifulSoup(zillow_data, 'html.parser')
test = soup.findAll("script", attrs={"type": "application/json"})
rent_data = test[1].text
rent_data = rent_data.replace('<!--', '')
rent_data = rent_data.replace('-->', '')
rent_data = json.loads(rent_data)
print(rent_data)
link_url = []
for i in rent_data['cat1']['searchResults']['listResults']:
    link = i["detailUrl"]
    link_url.append(link)
print(link_url)

for n in range(len(link_url)):
    if not link_url[n].startswith('https'):
        link_url[n] = "https://www.zillow.com" + link_url[n]
print(link_url)

price_list = []
for i in rent_data['cat1']['searchResults']['listResults']:
    try:
        price = i["price"]
        price_list.append(price)

    except KeyError:
        price = i["units"][0]["price"]
        price_list.append(price)
print(price_list)

address_list = []
for i in rent_data["cat1"]["searchResults"]["listResults"]:
    address = i["address"]
    address_list.append(address)
print(address_list)

# filling in the form
chrome_driver_path = 'C:\Development\chromedriver_win32\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get(url=GOOGLE_FORMS_LINK)
for i in range(len(link_url)):
    time.sleep(3)
    question_1 = driver.find_elements(By.CSS_SELECTOR, "div.Xb9hP input")[0]
    question_1.send_keys(address_list[i])

    question_2 = driver.find_elements(By.CSS_SELECTOR, "div.Xb9hP input")[1]
    question_2.send_keys(price_list[i])

    question_3 = driver.find_elements(By.CSS_SELECTOR, "div.Xb9hP input")[2]
    question_3.send_keys(link_url[i])

    submit = driver.find_element(By.CSS_SELECTOR, "div.lRwqcd div")
    submit.click()

    another_response = driver.find_element(By.LINK_TEXT, 'Submit another response')
    another_response.click()
