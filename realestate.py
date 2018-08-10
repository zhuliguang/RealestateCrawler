'''
Description: Grab sold house data from realestate.com.au
Author: Nan Li
Contact: linan.lqq0@gmail.com
'''

# import packages
import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


def readPostcode(file_name):
    os.chdir(os.path.dirname(__file__))
    postcode = pd.read_excel(file_name).sort_values(by=['Postcode'])
    postcode = postcode.values
    postcode = postcode[:,0]
    return postcode

def createUrl(postcode, page_no):
    url_pre = 'https://www.realestate.com.au/sold/in-'
    url = '{}{}/list-{}'.format(url_pre, postcode, page_no)
    return url
 
def extractUrl(url):
    try:
        r=requests.get(url)
        return r
    except:
        pass    
 
if __name__ == '__main__':
    file_name = 'Victoria.xlsx'
    postcode = readPostcode(file_name)
    url = createUrl(postcode[0], 1)
    list_page = requests.get(url).text
    soup = BeautifulSoup(list_page, 'html.parser')
    for house_link in soup.findAll('a', attrs={'href': re.compile
                        (r'/sold/property-\S+-vic-\S+[0-9]')}):
        house_url = 'https://www.realestate.com.au' + house_link.get('href')
        house_page = requests.get(house_url).text
        