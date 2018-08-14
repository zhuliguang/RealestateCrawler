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

# function to read postcode from excel file
def readPostcode(file_name):
    os.chdir(os.path.dirname(__file__))
    postcode = pd.read_excel(file_name).sort_values(by=['Postcode'])
    postcode = postcode.values
    postcode = postcode[:,0]
    return postcode

# function to create valid url
def createUrl(postcode, page_no):
    url_pre = 'https://www.realestate.com.au/sold/in-'
    url = '{}{}/list-{}?includeSurrounding=false'.format(url_pre, postcode, page_no)
    return url

# class to send request to web server
class Request:
    def __init__(self, url):
        self.url = url
        self.text = requests.get(self.url).text
        self.soup = BeautifulSoup(self.text, 'html.parser')

# class to extract infos from list page
class ExtractListPage(Request):
    def getNextPage(self):
        nextpage = self.soup.find('a', attrs={'title':'Go to Next Page'})
        return nextpage
    
    def getHouseLink(self):
        houselinks = self.soup.findAll('a', attrs={'href': re.compile(r'/sold/property-\S+-vic-\S+[0-9]')})
        return houselinks

# class to get house infos from house page
class House(Request):
    def getHouseID(self):
        house_id = self.soup.find('span', attrs={'class':'listing-metrics__property-id'})
        if house_id is not None:
            house_id = int(re.search(r'[0-9]+', house_id.text).group())
        return house_id

    def getAddress(self):
        address = self.soup.find('span', attrs={'class':'property-info-address__street'}).text
        return address

    def getSuburb(self):
        suburb_temp = self.soup.find('span', attrs={'class':'property-info-address__suburb'}).text
        suburb = re.search(r'[a-z|A-Z|\s]+,', suburb_temp).group()[:-1]
        post_code = re.search(r'[0-9]+', suburb_temp).group()
        return suburb, post_code

    def getHouseType(self):
        housetype = self.soup.find('span', attrs={'class':'property-info__property-type'}).text
        return housetype

    def getFeatures(self):
        bedroom = 0
        bathroom = 0
        parking = 0
        feature_str = ''
        for feature in self.soup.findAll('li', attrs={'class':'general-features__feature'}):
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
        return bedroom, bathroom, parking

    def getSoldPrice(self):
        soldprice = None
        soldprice_str = self.soup.find('span', attrs={'class':'property-price property-info__price'}).text
        price = re.search(r'[0-9,]+', soldprice_str)
        if price is not None:
            soldprice = int(price.group().replace(',', ''))
        return soldprice

    def getSoldDate(self):
        solddate = self.soup.find('p', attrs={'class':'property-info__secondary-content'})
        if solddate is not None:
            solddate = solddate.text[8:]
            try:
                solddate = datetime.strptime(solddate, '%d %b %Y')
            except:
                solddate = None
        return solddate
    
    def getAgency(self):
        agency = self.soup.find('p', attrs={'class':'agency-info__name'})
        if agency is not None:
            agency = agency.text
        return agency

    def getLocation(self):
        latitude = re.search(r'"latitude":-[0-9|.]+', self.text)
        if latitude is not None:
            latitude = -float(re.search(r'[0-9|.]+', latitude.group()).group())
        longitude = re.search(r'"longitude":[0-9|.]+', self.text)
        if longitude is not None:
            longitude = float(re.search(r'[0-9|.]+', longitude.group()).group())
        return latitude, longitude

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
        sql = """ CREATE TABLE victoria_test (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            house_id INTEGER UNIQUE,
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
            link VARCHAR(200),
            time TIMESTAMP ) """
        cursor = con.cursor()
        cursor.execute(sql)
        print('create table successfully!')
    except:
        print('table already exist!')
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
                    list_page = ExtractListPage(url)
                    break
                except:
                    time.sleep(5)
                    continue
            nextpage = list_page.getNextPage()
            houselinks = list_page.getHouseLink()
            for house_link in houselinks:
                house_url = 'https://www.realestate.com.au' + house_link.get('href')
                while True:
                    try:
                        house = House(house_url)
                        break
                    except:
                        time.sleep(5)
                        continue
                try:
                    # try to extract house infos from webpage
                    house_id = house.getHouseID()
                    address = house.getAddress()
                    suburb, post_code = house.getSuburb()
                    housetype = house.getHouseType()
                    bedroom, bathroom, parking = house.getFeatures()
                    soldprice = house.getSoldPrice()
                    solddate = house.getSoldDate()
                    agency = house.getAgency()
                    latitude, longitude = house.getLocation()
                    # save to mySQL database
                    sql = """INSERT INTO victoria_test (
                        house_id, address, suburb, postcode, house_type, bedroom, bathroom,
                        parking, sold_price, sold_date, agency, latitude, longitude, link, time) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"""
                    val = (house_id, address, suburb, post_code, housetype, bedroom, bathroom,
                        parking, soldprice, solddate, agency, latitude, longitude, house_url)
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