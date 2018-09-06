'''
Description: Scrape sold house data from realestate.com.au
Author: Nan Li
Contact: linan.lqq0@gmail.com
'''

# import packages
import os
import re
import time
import pandas as pd
import mysql.connector
from datetime import datetime
from mysql.connector import errorcode
from class_define import Request, ExtractListPage, House, LandInfo

os.chdir(os.path.dirname(__file__))

address_dict = ({'road':'rd', 'street':'st', 'place':'pl', 'avenue':'ave',
                'parade':'pde', 'highway':'hwy', 'drive':'dr', 'grove':'gr',
                'crescent':'cres', 'court':'ct', 'close':'cl', 'circuit':'cct',
                'avenue':'ave', 
                })

# function to read postcode from excel file
def readPostcode(file_name):
    postcode = pd.read_excel(file_name).sort_values(by=['Postcode'])
    postcode = postcode.values
    postcode = postcode[:,0]
    return postcode

# function to create valid url according to postcode
def createUrl(postcode, page_no):
    url_pre = 'https://www.realestate.com.au/sold/in-'
    if postcode < 1000:
        url = '{}0{}/list-{}?includeSurrounding=false'.format(url_pre, postcode, page_no)
    elif postcode < 10000:
        url = '{}{}/list-{}?includeSurrounding=false'.format(url_pre, postcode, page_no)
    else:
        print('Wrong postcode!!')
        exit()
    return url

# function to create valid url according to address
def createHouseUrl(address, suburb, postcode, use_short):
    url_pre = 'https://www.realestate.com.au/property/'
    str_address = address.lower()
    if re.search(r'[0-9|a-z]+/[0-9]', str_address) is not None:
        str_address = 'unit-' + str_address
    if use_short:
        for key in address_dict.keys():
            street_name = re.search(key, str_address)
            if street_name is not None:
                str_address = re.sub(street_name.group(), address_dict[key], str_address)
    str_suburb = suburb.lower()
    if postcode < 1000:
        str_postcode = 'nt-0{:d}'.format(postcode)
    elif postcode < 2600:
        str_postcode = 'nsw-{:d}'.format(postcode)
    elif postcode < 2700:
        str_postcode = 'act-{:d}'.format(postcode)
    elif postcode < 2800:
        str_postcode = 'nsw-{:d}'.format(postcode)
    elif postcode < 3000:
        str_postcode = 'act-{:d}'.format(postcode)
    elif postcode < 4000:
        str_postcode = 'vic-{:d}'.format(postcode)
    elif postcode < 5000:
        str_postcode = 'qld-{:d}'.format(postcode)
    elif postcode < 6000:
        str_postcode = 'sa-{:d}'.format(postcode)
    elif postcode < 7000:
        str_postcode = 'wa-{:d}'.format(postcode)
    elif postcode < 8000:
        str_postcode = 'tas-{:d}'.format(postcode)
    str_address = '{}-{}-{}'.format(str_address, str_suburb, str_postcode)
    str_address = re.sub('[,|\s|/]', '-', str_address)
    for _ in range(4):
        str_address = re.sub('--', '-', str_address)
    url = url_pre + str_address
    return url

def main(state, update):
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
        sql = """ CREATE TABLE {} (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            house_id INTEGER UNIQUE,
            address VARCHAR(100),
            suburb VARCHAR(50),
            postcode INTEGER,
            house_type VARCHAR(20),
            bedroom INTEGER,
            bathroom INTEGER,
            parking INTEGER,
            land_size INTEGER,
            floor_area INTEGER,
            year_built INTEGER,
            sold_price INTEGER,
            sold_date DATE,
            agency VARCHAR(100),
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            link VARCHAR(200),
            time TIMESTAMP ) """.format(state)
        cursor = con.cursor()
        cursor.execute(sql)
        print('create table successfully!')
    except:
        print('table already exist!')
        pass

    # scrape data according to postcode
    house_count = 0
    file_name = './Postcode/{}.xlsx'.format(state)
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
                    if post_code != postcode:
                        continue
                    housetype = house.getHouseType()
                    bedroom, bathroom, parking = house.getFeatures()
                    soldprice = house.getSoldPrice()
                    solddate = house.getSoldDate()
                    agency = house.getAgency()
                    latitude, longitude = house.getLocation()
                    # save to mySQL database
                    sql = """INSERT INTO {} (
                        house_id, address, suburb, postcode, house_type, bedroom, bathroom,
                        parking, sold_price, sold_date, agency, latitude, longitude, link, time) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())""".format(state)
                    val = (house_id, address, suburb, post_code, housetype, bedroom, bathroom,
                        parking, soldprice, solddate, agency, latitude, longitude, house_url)
                    cursor.execute(sql, val)
                    con.commit()
                    house_count = house_count + 1
                    print(house_count, datetime.now())
                except:
                    if update:
                        nextpage = None
                        break
                    else:
                        file = open('url_with_problem.log', 'a')
                        file.write(house_url + '\n')
                        print('error', datetime.now())
                        continue
            if nextpage is not None:
                page = page + 1
            else:
                break
    con.close()
    print('Mission completed!!!')

def update():
    main('australian_capital_territory', True)
    main('new_south_wales', True)
    main('northern_territory', True)
    main('queensland', True)
    main('south_australia', True)
    main('tasmania', True)
    main('victoria', True)
    main('western_australia', True)

def addLandInfo(state):
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
    sql = """ SELECT house_id, address, suburb, postcode, id FROM {}
            WHERE land_size is null
            ORDER BY id""".format(state)
    select_cursor = con.cursor(dictionary=True, buffered=True)
    update_cursor = con.cursor()
    select_cursor.execute(sql)
    while True:
        address = select_cursor.fetchone()
        if address == None:
            break
        url = createHouseUrl(address['address'], address['suburb'], address['postcode'], True)
        land_info = LandInfo(url)
        if land_info.status_code == 200:
            page_exist = land_info.soup.find('table', attrs={'class':'info-table'})
            if page_exist is None:
                url = createHouseUrl(address['address'], address['suburb'], address['postcode'], False)
                land_info = LandInfo(url)
                if land_info.status_code == 400:
                    break
            land_size, floor_area, year_built = land_info.getLandInfo()
            print(land_info.getLandInfo(), url, datetime.now())
            # save to mySQL database
            insert_sql = """UPDATE {} SET land_size = %s
                WHERE house_id = %s""".format(state)
            insert_val = (land_size, address['house_id'])
            update_cursor.execute(insert_sql, insert_val)
            insert_sql = """UPDATE {} SET floor_area = %s
                WHERE house_id = %s""".format(state)
            insert_val = (floor_area, address['house_id'])
            update_cursor.execute(insert_sql, insert_val)
            insert_sql = """UPDATE {} SET year_built = %s
                WHERE house_id = %s""".format(state)
            insert_val = (year_built, address['house_id'])
            update_cursor.execute(insert_sql, insert_val)
            con.commit()
            time.sleep(0.001)
        elif land_info.status_code == 400:
            break
    con.close()
    print('ip interrupted', land_info.header_no, datetime.now())
    print('Mission completed!!!')

def testConnection():
    while True:
        url = 'https://www.realestate.com.au/property/lookup?id=4150213'
        land_info = LandInfo(url)
        if land_info.status_code == 200:
            url = land_info.redir_url
            land_info = LandInfo(url)
            if land_info.status_code == 200:
                print(land_info.header_no, land_info.getLandInfo(), datetime.now())
                time.sleep(0.001)
            elif land_info.status_code == 400:
                break
        elif land_info.status_code == 400:
            break
    verification_code = land_info.soup.find('div', attrs={'id':'challengeQuestion'}).text
    verification_code = re.search('[0-9]+', verification_code).group()
    print(land_info.header_no, verification_code)

if __name__ == '__main__':
    #update()
    #addLandInfo('victoria')
    #testConnection()
    url = 'https://www.realestate.com.au/property/lookup?id=4150213'
    land_info = LandInfo(url)
    if land_info.status_code == 200:
        url = land_info.redir_url
        land_info = LandInfo(url)
        if land_info.status_code == 200:
            print(land_info.header_no, land_info.getLandInfo(), datetime.now())