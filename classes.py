'''
Description: Definitions of classes
Author: Nan Li
Contact: linan.lqq0@gmail.com
'''

# import packages
import re
import requests
from random import randrange
from datetime import datetime
from bs4 import BeautifulSoup

# class to send request to web server
class Request:
    def __init__(self, url):
        self.url = url
        self.redir_url = None
        randnum = randrange(53)
        if randnum == 0:   # Macbook
            self.header = ({'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' , 
                            'cookie': 'mmp_ttl=c6312b25eaae3d70278fcb28ca1424d7'})
        elif randnum == 1: # AAAT
            self.header = ({'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' , 
                            'cookie': 'mmp_ttl=05e15662ccbf6a39c5f8ad5e2ac5f9e6'})
        elif randnum == 2: # Android 4.0.2
            self.header = ({'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                            'cookie': 'mmp_ttl=0f9a3e351141144f956e93338b160bf3'})
        elif randnum == 3: # Blackberry BB10
            self.header = ({'User-Agent': 'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.1+ (KHTML, like Gecko) Version/10.0.0.1337 Mobile Safari/537.1+',
                            'cookie': 'mmp_ttl=ca11cb3c5dc5af4efb3717a453f92157'})
        elif randnum == 4: # Safari Mac
            self.header = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
                            'cookie': 'mmp_ttl=fbec7f359e8e7f5afc8e25819ec02a4c'})
        elif randnum == 5: # Firefox Android mobile
            self.header = ({'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:46.0) Gecko/46.0 Firefox/46.0',
                            'cookie': 'mmp_ttl=cc1c284be2d864559bea20aeb068e65c'})
        elif randnum == 6: # IE11
            self.header = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                            'cookie': 'mmp_ttl=5af315c3c2ec68e9496f43a3d42b372c'})
        elif randnum == 7: # Opera Mac
            self.header = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.31',
                            'cookie': 'mmp_ttl=fae1b4f10bdb9584e46e4420d2d84086'})
        elif randnum == 8: # UC Android
            self.header = ({'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.4.4; en-US; XT1022 Build/KXC21.5-40) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.7.0.636 U3/0.8.0 Mobile Safari/534.30',
                            'cookie': 'mmp_ttl=76f23b2ba7b3898750883276d301ed24'})
        elif randnum == 9: # Safari iPad
            self.header = ({'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1',
                            'cookie': 'mmp_ttl=bc48ac913a52061d6bf45b20f9b09a33'})
        elif randnum == 10: # Android 2.3
            self.header = ({'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                            'cookie': 'mmp_ttl=ae0c75026c27f1f2e54cedee382d84a2'})
        elif randnum == 11: # Blackberry Playbook2.1
            self.header = ({'User-Agent': 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML, like Gecko) Version/7.2.1.0 Safari/536.2+',
                            'cookie': 'mmp_ttl=88b42190d1173395d8c0e8f849b8dd35'})
        elif randnum == 12: # Blackberry 9900
            self.header = ({'User-Agent': 'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.187 Mobile Safari/534.11+',
                            'cookie': 'mmp_ttl=71e912871ca3028338b96c105bba9dcf'})
        elif randnum == 13: # Chrome Android mobile
            self.header = ({'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36',
                            'cookie': 'mmp_ttl=d5cabcd05f19fcccde1e0f2f911d7096'})
        elif randnum == 14: # Chrome Android tablet
            self.header = ({'User-Agent': 'Mozilla/5.0 (Linux; Android 4.3; Nexus 7 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                            'cookie': 'mmp_ttl=2afc9b9fefc9cac6cd57c55bb0a58265'})
        elif randnum == 15: # Firefox iPhone
            self.header = ({'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4',
                            'cookie': 'mmp_ttl=3ff70af2f331232c52e47c8cc402ffbb'})
        elif randnum == 16: # Chrome iPad
            self.header = ({'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/68.0.3440.106 Mobile/13B143 Safari/601.1.46',
                            'cookie': 'mmp_ttl=76eb79b278066d1dddeb0e994ed9db1a'})
        elif randnum == 17: # Chrome Chrome OS
            self.header = ({'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                            'cookie': 'mmp_ttl=f1e9ce9fc87d6ca41454074dfad81532'})
        elif randnum == 18: # Chrome Mac
            self.header = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                            'cookie': 'mmp_ttl=818357bb46740ac3fdd646308e83b90c'})
        elif randnum == 19: # Chrome Windows
            self.header = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                            'cookie': 'mmp_ttl=5a31d4b7820e8cdb92bc82718fbb9fd2'})
        elif randnum == 20: # Firefox Android tablet
            self.header = ({'User-Agent': 'Mozilla/5.0 (Android 4.4; Tablet; rv:46.0) Gecko/46.0 Firefox/46.0',
                            'cookie': 'mmp_ttl=7525f5c8dfe5c29ec302aa83d94f4e65'})
        elif randnum == 21: # Firefox iPhone
            self.header = ({'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4',
                            'cookie': 'mmp_ttl=54ea6ba70dfa757e715d276edbaad643'})
        elif randnum == 22: # Firefox iPad
            self.header = ({'User-Agent': 'Mozilla/5.0 (iPad; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4',
                            'cookie': 'mmp_ttl=6a5f9c9362ebabb2def019010025058f'})
        elif randnum == 23: # Firefox Mac
            self.header = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
                            'cookie': 'mmp_ttl=c2732380c6f7fe7696363ceb29eb6e93'})
        elif randnum == 24: # Firefox Windows
            self.header = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
                            'cookie': 'mmp_ttl=4e48f0ad60fd4913139c54bca422ce83'})
        elif randnum == 25: # IE10
            self.header = ({'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                            'cookie': 'mmp_ttl=24e2f875b15c15c75234d4cf49fa7009'})
        elif randnum == 26: # IE9
            self.header = ({'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
                            'cookie': 'mmp_ttl=b753917c738613e3e22b613d004f84eb'})
        elif randnum == 27: # IE8
            self.header = ({'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
                            'cookie': 'mmp_ttl=6b7e7cad9ccae75af4ad2648f4f9e70d'})
        elif randnum == 28: # IE7
            self.header = ({'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
                            'cookie': 'mmp_ttl=ab547322857155c6facf24b6282cffbd'})
        elif randnum == 29: # Opera presto Mac
            self.header = ({'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.9.1) Presto/2.12.388 Version/12.16',
                            'cookie': 'mmp_ttl=416b21e6ee4cfa6b40030325f38c321e'})
        elif randnum == 30: # Opera presto Windows
            self.header = ({'User-Agent': 'Opera/9.80 (Windows NT 6.1) Presto/2.12.388 Version/12.16',
                            'cookie': 'mmp_ttl=705698c551d6b4d3d70a947f4e4cfaef'})
        elif randnum == 31: # Opera mobile android
            self.header = ({'User-Agent': 'Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02',
                            'cookie': 'mmp_ttl=464390594c26ade08ded82ebfa325300'})
        elif randnum == 32: # Opera iOS
            self.header = ({'User-Agent': 'Opera/9.80 (iPhone; Opera Mini/8.0.0/34.2336; U; en) Presto/2.8.119 Version/11.10',
                            'cookie': 'mmp_ttl=777e9b1d288880f1e2ce5b38227a47dd'})
        elif randnum == 33: # Safari iPhone
            self.header = ({'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1',
                            'cookie': 'mmp_ttl=1e0ec23f4bbfe4e0f5e10a0b825007cf'})
        elif randnum == 34: # UC iOS
            self.header = ({'User-Agent': 'UCWEB/2.0 (iPad; U; CPU OS 7_1 like Mac OS X; en; iPad3,6) U2/1.0.0 UCBrowser/9.3.1.344',
                            'cookie': 'mmp_ttl=8c5a4e592d6e791d7a4e6d7d1ab7a285'})
        elif randnum == 35: # UC Windows phone
            self.header = ({'User-Agent': 'NokiaX2-02/2.0 (11.79) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2;.NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2) UCBrowser8.4.0.159/70/352',
                            'cookie': 'mmp_ttl=4890bf84fabab0145001671830f121b0'})
        elif randnum == 36: # Android 2.3
            self.header = ({'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                            'cookie': 'mmp_ttl=136711978f83c131724ca6aeb9fec3c7'})
        elif randnum == 37: # Blackberry BB10
            self.header = ({'User-Agent': 'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.1+ (KHTML, like Gecko) Version/10.0.0.1337 Mobile Safari/537.1+',
                            'cookie': 'mmp_ttl=3cfbccaad308b0d25fd3c5eea7317165'})
        elif randnum == 38: # Safari Mac
            self.header = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
                            'cookie': 'mmp_ttl=50f1b2ef9d9529d06a4707892f9b99d7'})
        elif randnum == 39: # Firefox Android mobile
            self.header = ({'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:46.0) Gecko/46.0 Firefox/46.0',
                            'cookie': 'mmp_ttl=0e4eeae8996710aad548750a119268e7'})
        elif randnum == 40: # IE11
            self.header = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                            'cookie': 'mmp_ttl=d1273bdda01496b3e78e1194531a2585'})
        elif randnum == 41: # Opera Mac
            self.header = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.31',
                            'cookie': 'mmp_ttl=031fbafdbacb104933041c633bb0938c'})
        elif randnum == 42: # UC Android
            self.header = ({'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.4.4; en-US; XT1022 Build/KXC21.5-40) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.7.0.636 U3/0.8.0 Mobile Safari/534.30',
                            'cookie': 'mmp_ttl=d56f5511dd2c9d5f6aa2756f95561c0f'})
        elif randnum == 43: # Safari iPad
            self.header = ({'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1',
                            'cookie': 'mmp_ttl=2d7e61bc3538188a6aa449cfc8f44d34'})
        elif randnum == 44: # Blackberry Playbook2.1
            self.header = ({'User-Agent': 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML, like Gecko) Version/7.2.1.0 Safari/536.2+',
                            'cookie': 'mmp_ttl=bb7111e56480678f093e9790d70fcb97'})
        elif randnum == 45: # Blackberry 9900
            self.header = ({'User-Agent': 'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.187 Mobile Safari/534.11+',
                            'cookie': 'mmp_ttl=fe1006cc968a972289a0802e6e89d6d1'})
        elif randnum == 46: # Chrome Android mobile
            self.header = ({'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36',
                            'cookie': 'mmp_ttl=df693a5a164a6c4f6124b8a3054b7234'})
        elif randnum == 47: # Chrome iPhone
            self.header = ({'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/68.0.3440.106 Mobile/13B143 Safari/601.1.46',
                            'cookie': 'mmp_ttl=360fa4999b516915570f3cd55acb6e9d'})
        elif randnum == 48: # Chrome iPad
            self.header = ({'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/68.0.3440.106 Mobile/13B143 Safari/601.1.46',
                            'cookie': 'mmp_ttl=48fbbbcde08f3705b6c3ae9897ec7ac1'})
        elif randnum == 49: # Chrome Chrome OS
            self.header = ({'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                            'cookie': 'mmp_ttl=e1313f5b5c83b4b39f55923d7499765d'})
        elif randnum == 50: # Chrome Mac
            self.header = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                            'cookie': 'mmp_ttl=f61eb84236d2e84d3fa20619c1968256'})
        elif randnum == 51: # Chrome Windows
            self.header = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                            'cookie': 'mmp_ttl=b4125d64b0ae001c76ad6057d70f2f98'})
        elif randnum == 52: # Firefox Android tablet
            self.header = ({'User-Agent': 'Mozilla/5.0 (Android 4.4; Tablet; rv:46.0) Gecko/46.0 Firefox/46.0',
                            'cookie': 'mmp_ttl=64f53cfacd910fa7d22c8cfe5f115bdc'})
        resp = requests.get(url=self.url, headers=self.header)
        for r in resp.history:
            self.redir_url = r.headers['Location']
        self.header_no = randnum
        self.status_code = resp.status_code
        self.text = resp.text
        self.soup = BeautifulSoup(self.text, 'html.parser')

# class to extract infos from list page
class ExtractListPage(Request):
    def getNextPage(self):
        nextpage = self.soup.find('a', attrs={'title':'Go to Next Page'})
        return nextpage
    
    def getHouseLink(self):
        houselinks = self.soup.findAll('a', attrs={'href': re.compile(r'/sold/property-\S+-[a-z|-|+]+-[0-9]')})
        return houselinks

# class to get house infos from house page
class House(Request):
    def getHouseID(self):
        house_id = self.soup.find('span', attrs={'class':'listing-metrics__property-id'})
        if house_id is not None:
            house_id = int(re.search(r'[0-9]+', house_id.text).group())
        return house_id

    def getREAID(self):
        REA_id = re.search('\"propertyId\":\"[0-9]+\"', self.text)
        if REA_id is not None:
            REA_id = int(re.search(r'[0-9]+', REA_id.group()).group())
        return REA_id

    def getAddress(self):
        address = self.soup.find('span', attrs={'class':'property-info-address__street'}).text
        return address

    def getSuburb(self):
        suburb_temp = self.soup.find('span', attrs={'class':'property-info-address__suburb'}).text
        suburb = re.search(r'[a-z|A-Z|\s]+,', suburb_temp).group()[:-1]
        post_code = re.search(r'[0-9]+', suburb_temp).group()
        return suburb, int(post_code)

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

class LandInfo(Request):
    def getLandInfo(self):
        land_info = self.soup.find('table', attrs={'class':'info-table'})
        land_size = 0
        floor_area = 0
        year_built = 0
        if land_info is not None:
            land_info = land_info.text
            land_size = re.search(r'Land size\s+[0-9]+\s', land_info)
            if land_size is not None:
                land_size = int(re.search(r'[0-9]+', land_size.group()).group())
            else:
                land_size = 0
            floor_area = re.search(r'Floor area\s+[0-9]+\s', land_info)
            if floor_area is not None:
                floor_area = int(re.search(r'[0-9]+', floor_area.group()).group())
            else:
                floor_area = 0
            year_built = re.search(r'Year built\s+[0-9]+', land_info)
            if year_built is not None:
                year_built = int(re.search(r'[0-9]+', year_built.group()).group())
            else:
                year_built = 0
        return land_size, floor_area, year_built