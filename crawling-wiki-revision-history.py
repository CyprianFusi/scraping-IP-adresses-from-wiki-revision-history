#Crawling and scraping IP addresses from wikipedia revision history pages
#
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import datetime as dt
import random
import re

rootUrl = 'http://en.wikipedia.org'
articleUrl = '/wiki/Python_(programming_language)'
access_key = '<Register and get an access_key from api.ipstack.com and use that here>'

def getLinks(articleUrl):
    page = urlopen(f'{rootUrl}{articleUrl}')
    html = BeautifulSoup(page, 'html.parser')
    hrefRegex = re.compile('^(/wiki/)((?!:).)*$')                      # links on wikipedia begin with /wiki/
    aTagEles = html.find(id = 'bodyContent').findAll('a', href = hrefRegex)
    return aTagEles

def getHistoryIPs(linkUrl):
    #Format of revision history url: https://en.wikipedia.org/w/index.php?title=<Title_in_URL>&action=history
    title = linkUrl.replace('/wiki/', '')     # /wiki/Python_(programming_language) becomes Python_(programming_language)
    historyUrl = f'{rootUrl}/w/index.php?title={title}&action=history'   # construct history url from each link
    page = urlopen(historyUrl)
    html = BeautifulSoup(page, 'html.parser')
    bdiTagEles = html.findAll('bdi')                              # IP addresses were embeded in <bdi> tags, (may change)
    ipAddressList = []
    ipRegex = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")  # regex to match IP addresses
    for bdiTagEle in bdiTagEles:
        ip = ipRegex.findall(bdiTagEle.get_text())
        if ip not in ipAddressList:
            ipAddressList.append(ip)
    return ipAddressList

def getLocationDetails(ipAddress):
    try:
        response = urlopen(f'http://api.ipstack.com/{ipAddress}?access_key={access_key}').read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    city, country, code = responseJson.get('city'), responseJson.get('country_name'), responseJson.get('country_code')
    return [city, country, code]

aTagEles = getLinks(articleUrl)
while(len(aTagEles) > 0):
    for aTagEle in aTagEles:
        ipAddressList = getHistoryIPs(aTagEle.attrs['href'])
        for ipAddress in ipAddressList:
            if ipAddress:
                country_data = getLocationDetails(ipAddress[0])
                if country_data:
                    print(f'The IP address {ipAddress[0]} is from {country_data[0]}, {country_data[1]} ({country_data[2]})')
    newLink = aTagEles[random.randint(0, len(aTagEles) - 1)].attrs['href']    # randomly select a new starting page
    aTagEles = getLinks(newLink)             # the crawling process
