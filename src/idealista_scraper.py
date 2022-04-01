import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager


def parse_url(url, driver, captcha = False):
    try:
        driver.get(url)
        if (captcha):
            input("Press ENTER after filling CAPTCHA")
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
    except Exception as e:
        print("Error:", str(e))
        content = None
        soup = None

    return content, soup


if __name__ == '__main__':
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    url_base = "https://www.idealista.com"
    url = url_base + "/venta-viviendas/barcelona/sant-andreu/mapa"
    content, soup = parse_url(url, driver, True)
    # items = soup.find_all('div', class_="item-info-container")
    items = soup.find_all('ul', id="sublocations")

    for item in items:
        links = item.find_all('a')
        for link in links:
            url = url_base + link.get('href')
            print(url)
            time.sleep(1)
            sub_content, sub_soup = parse_url(url, driver, False)

            containers = sub_soup.find_all('div', class_="item-info-container")
            sub_items = []
            for container in containers:
                price = container.find_all('span', class_="item-price")[0].text
                room = container.find_all('span', class_="item-detail")[0].text
                space = container.find_all('span', class_="item-detail")[1].text
                name = container.find_all('a', class_="item-link")[0].text
                link = url_base + container.find_all('a', class_="item-link")[0].get('href')
                sub_items.append([price, room, space, name, link])
            
            with open('housing-barcelona.csv', 'a', newline='') as f:
                write = csv.writer(f)
                for sub_item in sub_items:
                    write.writerow(sub_item)


            
            

