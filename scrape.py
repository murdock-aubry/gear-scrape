import requests
import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def scrape_gears(url):
    data_total = []

    # Set up the Chrome WebDriver
    options = Options()
    options.headless = True  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)

    

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 's1')))
    WebDriverWait(driver, 10).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "#s1 option")) > 0)


    html = driver.page_source

    try:
        soup = BeautifulSoup(html, 'html.parser')
        type_element = soup.find('h1', {'class': 'bigtit'})
        if type_element is None:
            # Element not found, try the alternative
            type_element = soup.find('div', {'class': 'bigtit'})
        gear_type = type_element.get_text() if type_element else 'Not Found'
    except Exception as e:
        print(f"An error occurred: {e}")
        gear_type = 'Not Found'

    select_element = driver.find_element(By.ID, 's1')
    select = Select(select_element)

    for option in select.options:
        value = option.get_attribute('value')


        if value:
            select.select_by_visible_text(value)

            material = value

            time.sleep(1)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Extract gear type
            thead = soup.find('thead', {'id': 'thead'})  # Find the specific thead
            headers = thead.find_all('tr')  # Find all <tr> elements within the thead
            html_headers = str(headers[0])  # Convert the first row of headers to a string
            soup_headers = BeautifulSoup(html_headers, 'html.parser')
            header_names = [th.get_text().strip() for th in soup_headers.find_all('th')]  # Use soup_headers to limit the search


            # Extract header names
            thead = soup.find('thead', {'id': 'thead'})  # Find the specific thead
            headers = thead.find_all('tr')  # Find all <tr> elements within the thead
            html_headers = str(headers[0])  # Convert the first row of headers to a string
            soup_headers = BeautifulSoup(html_headers, 'html.parser')
            header_names = [th.get_text().strip() for th in soup_headers.find_all('th')]  # Use soup_headers to limit the search


            tbody = soup.find('tbody', {'id': 'tbody'})

            # Check if tbody exists
            if tbody:
                # Find all rows within the <tbody>
                rows = tbody.find_all('tr')


                for row in rows:
                    # Extract columns from the row
                    columns = row.find_all('td')
                    data = [col.text.strip() for col in columns]
                    new_gear = make_new_gear(gear_type, material, header_names, data)
                    data_total.append(new_gear)

    driver.quit()

    return data_total 


def scrape_gears2(urls):

    new_gears = []

    ngears = len(urls)

    # Set up the Chrome WebDriver
    options = Options()
    options.headless = True  # Run in headless mode (no GU
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    for iurl, url in enumerate(urls):
        driver.get(url)



        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 's1')))
        WebDriverWait(driver, 10).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "#s1 option")) > 0)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # # Extract gear header info
        try:
            hinfo = soup.find('h1', {'id': 'category'}).get_text()  # Find the specific thead
        except Exception as e:
            try:
                hinfo = soup.find('div', {'id': 'category'}).get_text()  # Find the specific thead
            except Exception as e:
                hinfo = "N/A"
        
        # Extract header names
        thead = soup.find('div', {'id': 'info_area'})  # Find the specific thead
        table = thead.find_all('tr')  # Find all <tr> elements within the thead

        if len(table) == 0:
            thead = soup.find('div', {'id': 'infos'})  # Find the specific thead
            table = thead.find_all('tr')  # Find all <tr> elements within the thead

        html_table = str(table)  # Convert the first row of headers to a string
        soup_table = BeautifulSoup(html_table, 'html.parser')
        headers = [th.get_text().strip() for th in soup_table.find_all('th')]  # Use soup_headers to limit the search
        # data = [td.get_text().strip() for td in soup_table.find_all('td')]
        
        data = []
        
        for td in soup_table.find_all('td'):
            text = str(td.get_text().strip())
            data.append(text)

        # print(len(headers) == len(data))
        # print(len(headers), len(data))
        # print(headers)
        # print("")
        # print(data)



        # if len(headers) == len(data):

        new_gear = make_new_gear2(headers[:len(data)], hinfo, data)
        new_gears.append(new_gear)

        print(f"Gear {iurl + 1} of {ngears}")
    return new_gears


def get_dxf_file(catalog_numbers, catalog_url):
    download_dir = "/Users/murdockaubry/Library/Mobile Documents/com~apple~CloudDocs/Research/Personal Research/gear-gen/gear_dxf"

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,  # Set the download directory
        "download.prompt_for_download": False,       # Disable "Save As" dialog
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    chrome_options.add_argument("--headless")
    service = Service("/usr/local/bin/chromedriver")  # Replace with the path to your ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    ngears = len(catalog_numbers)

    for igear in range(ngears):

        url = "https://khkgears2.net/" + catalog_url[igear] + "/" + catalog_numbers[igear]  # Replace with your URL

        
        driver.get(url)
        
        time.sleep(1.5)


        dxf_button = driver.find_element(By.ID, "cds-download-dxf-button")
        dxf_button.click()



def make_new_gear(gear_type, material, headers, data):

    gear = {}

    gear["Type"] = gear_type
    gear["Material Name"] = material
    for iheader, header in enumerate(headers):
        gear[header] = data[iheader]

    gear["DXF path"] = f'gear_dxf/{data[0]}'

    return gear


def make_new_gear2(headers, info, data):

    gear = {}


    gear["info"] = info
    for iheader, header in enumerate(headers):
        gear[header] = data[iheader]

    path = f'gear_dxf/{data[0]}'

    gear["DXF path"] = path



    return gear
