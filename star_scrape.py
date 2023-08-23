from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

url = 'https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars'

browser = webdriver.Edge()
browser.get(url)

time.sleep(1)

scraped_data = []

def scrape():
    data = BeautifulSoup(browser.page_source, 'html.parser')

    #Finding table
    star_table = data.find('table', attrs={'class' : 'wikitable'})

    #Finding T body
    t_body = star_table.find('tbody')

    #Finding Tr tags
    rows = t_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        #print(cols)

        temp_list = []

        for col in cols:
            #print(col.get_text())   
            data = col.get_text(strip=True)
            print(data)
            temp_list.append(data)
        
        #Appending to scraped data
        scraped_data.append(temp_list)

def Make_CSV(scraped_data):
    stars_data = []

    for i in range(0, len(scraped_data)):
        star_names = scraped_data[i][1]
        distance = scraped_data[i][3]
        mass = scraped_data[i][5]
        radius = scraped_data[i][6]
        lum = scraped_data[i][7]

        required_data = [star_names, distance, mass, radius, lum]
        stars_data.append(required_data)

    #Headers
    header = ['Star_Name', 'Distance', 'Mass', 'Radius', 'Luminosity']

    #Panda Dataframe
    star_data_df = pd.DataFrame(stars_data, columns=header)

    #converting to CSV
    star_data_df.to_csv('scraped_data.csv', index=True, index_label='id')

scrape()
Make_CSV(scraped_data)