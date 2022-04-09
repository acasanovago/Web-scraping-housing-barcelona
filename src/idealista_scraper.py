import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

URL_BASE = "https://www.idealista.com"
MAX_PAGES = 5
SLEEP = 1
PATH = './csv/housing-barcelona.csv'
WAIT_CAPTCHA = True

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

def navigate_next_link(link):
    url = URL_BASE + link.get('href')
    print(url)
    time.sleep(SLEEP)
    content, soup = parse_url(url, driver, False)
    page_info = get_page_info(url)
    return soup, page_info

def get_page_info(url):
    page_info = url\
        .replace("/venta-viviendas/", "")\
        .replace("pagina-", "")\
        .replace("mapa", "1")\
        .replace(".html", "") \
        .replace(".htm", "") \
        .replace(URL_BASE, "") \
        .split("/")
    if len(page_info) == 4:
        print(page_info)
        return page_info
    else:
        print("Error: invalid url")
        return ["error", "error", "error", "error"]


def search_data_in_link(soup, items, page_info):
    containers = soup.find_all('div', class_="item-info-container")

    for container in containers:
        price = container.find_all('span', class_="item-price")[0].text
        room = container.find_all('span', class_="item-detail")[0].text
        space = container.find_all('span', class_="item-detail")[1].text
        name = container.find_all('a', class_="item-link")[0].text
        link = URL_BASE + container.find_all('a', class_="item-link")[0].get('href')
        items.append([price, room, space, name, link, page_info[0], page_info[1], page_info[2], page_info[3]])

    return items

def get_data_in_pages(soup, items):
    pagination = soup.find_all('div', class_="pagination")
    if pagination:
        pages = pagination[0].find_all('a')

        for page in pages:
            if page.text != "Siguiente" and int(page.text) <= MAX_PAGES:
                page_soup, page_info = navigate_next_link(page)
                items = search_data_in_link(page_soup, items, page_info)

    return items


def to_csv(path, sub_items):
    with open(path, 'w', newline='') as f:
        write = csv.writer(f)
        cols = ['price', 'room', 'space', 'name', 'link', 'city', 'area', 'subarea', 'page']
        write.writerow(cols)
        for sub_item in sub_items:
            write.writerow(sub_item)

if __name__ == '__main__':
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    locations = ["/venta-viviendas/barcelona/nou-barris/mapa", "/venta-viviendas/barcelona/sant-andreu/mapa", "/venta-viviendas/barcelona/sant-marti/mapa"]
    items = []
    wait_captcha = WAIT_CAPTCHA
    for location in locations:
        url = URL_BASE + location
        content, soup = parse_url(url, driver, wait_captcha)
        wait_captcha = False
        sublocations = soup.find_all('ul', id="sublocations")

        for sublocation in sublocations:
            links = sublocation.find_all('a')
            for link in links:
                sub_soup, page_info = navigate_next_link(link)
                items = search_data_in_link(sub_soup, items, page_info)
                get_data_in_pages(sub_soup, items)

    to_csv(PATH, items)