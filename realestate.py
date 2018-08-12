'''
Description: Scrape sold house data from realestate.com.au
Author: Nan Li
Contact: linan.lqq0@gmail.com
'''

# import packages
import os
import re
import time
import requests
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
from bs4 import BeautifulSoup


def readPostcode(file_name):
    os.chdir(os.path.dirname(__file__))
    postcode = pd.read_excel(file_name).sort_values(by=['Postcode'])
    postcode = postcode.values
    postcode = postcode[:,0]
    return postcode

def createUrl(postcode, page_no):
    url_pre = 'https://www.realestate.com.au/sold/in-'
    url = '{}{}/list-{}?includeSurrounding=false'.format(url_pre, postcode, page_no)
    return url

 
if __name__ == '__main__':
    # connect mySQL database
    try:
        con=mysql.connector.connect(user='root',password='asdfghjkl;\'',database='aus_sold_houses')
        print("Database connected sucessfully!")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        exit()
    # create table if not exist
    try:
        sql = """ CREATE TABLE house_info_main (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            house_id INTEGER,
            address VARCHAR(100),
            suburb VARCHAR(50),
            postcode INTEGER,
            house_type VARCHAR(20),
            bedroom INTEGER,
            bathroom INTEGER,
            parking INTEGER,
            sold_price INTEGER,
            sold_date DATE,
            agency VARCHAR(100),
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            link VARCHAR(200) ) """
        cursor = con.cursor()
        cursor.execute(sql)
    except:
        pass
    # scrape data according to postcode
    house_count = 0
    file_name = 'Victoria.xlsx'
    postcodes = readPostcode(file_name)
    for postcode in postcodes:
        print(postcode)
        page = 1
        while True:
            url = createUrl(postcode, page)
            while True:
                try:
                    list_page = requests.get(url).text
                    break
                except:
                    time.sleep(5)
                    continue
            list_soup = BeautifulSoup(list_page, 'html.parser')
            nextpage = list_soup.find('a', attrs={'title':'Go to Next Page'})
            for house_link in list_soup.findAll('a', attrs={'href': re.compile
                                (r'/sold/property-\S+-vic-\S+[0-9]')}):
                house_url = 'https://www.realestate.com.au' + house_link.get('href')
                while True:
                    try:
                        house_page = requests.get(house_url).text
                        break
                    except:
                        time.sleep(5)
                        continue
                house_soup = BeautifulSoup(house_page, 'html.parser')
                house_id = house_soup.find('span', attrs={'class':'listing-metrics__property-id'})
                if house_id is not None:
                    house_id = int(re.search(r'[0-9]+', house_id.text).group())
                try:
                    address = house_soup.find('span', attrs={'class':'property-info-address__street'}).text
                    suburb_temp = house_soup.find('span', attrs={'class':'property-info-address__suburb'}).text
                    suburb = re.search(r'[a-z|A-Z|\s]+,', suburb_temp).group()[:-1]
                    post_code = re.search(r'[0-9]+', suburb_temp).group()
                    housetype = house_soup.find('span', attrs={'class':'property-info__property-type'}).text
                    bedroom = 0
                    bathroom = 0
                    parking = 0
                    feature_str = ''
                    for feature in house_soup.findAll('li', attrs={'class':'general-features__feature'}):
                        feature_str = feature_str + feature.get('aria-label')
                    bed = re.search(r'[0-9]+\sbedroom', feature_str)
                    if bed is not None:
                        bedroom = int(re.search(r'[0-9]+', bed.group()).group())
                    bath = re.search(r'[0-9]+\sbathroom', feature_str)
                    if bath is not None:
                        bathroom = int(re.search(r'[0-9]+', bath.group()).group())
                    park = re.search(r'[0-9]+\sparking space', feature_str)
                    if park is not None:
                        parking = int(re.search(r'[0-9]+', park.group()).group())
                    soldprice = None
                    soldprice_str = house_soup.find('span', attrs={'class':'property-price property-info__price'}).text
                    price = re.search(r'[0-9,]+', soldprice_str)
                    if price is not None:
                        soldprice = int(price.group().replace(',', ''))
                    solddate = house_soup.find('p', attrs={'class':'property-info__secondary-content'})
                    if solddate is not None:
                        solddate = solddate.text[8:]
                        try:
                            solddate = datetime.strptime(solddate, '%d %b %Y')
                        except:
                            solddate = None
                    agent = house_soup.find('p', attrs={'class':'agency-info__name'})
                    if agent is not None:
                        agent = agent.text
                    latitude = re.search(r'"latitude":-[0-9|.]+', house_page)
                    if latitude is not None:
                        latitude = -float(re.search(r'[0-9|.]+', latitude.group()).group())
                    longitude = re.search(r'"longitude":[0-9|.]+', house_page)
                    if longitude is not None:
                        longitude = float(re.search(r'[0-9|.]+', longitude.group()).group())
                    # save to mySQL database
                    sql = """INSERT INTO house_info_main (
                        house_id, address, suburb, postcode, house_type, bedroom, bathroom,
                        parking, sold_price, sold_date, agency, latitude, longitude, link) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    val = (house_id, address, suburb, post_code, housetype, bedroom, bathroom,
                        parking, soldprice, solddate, agent, latitude, longitude, house_url)
                    cursor.execute(sql, val)
                    con.commit()
                    house_count = house_count + 1
                    print(house_count)
                except:
                    file = open('url_with_problem.log', 'a')
                    file.write(house_url + '\n')
                    continue
            if nextpage is not None:
                page = page + 1
            else:
                break
    con.close()
    print('Mission completed!!!')