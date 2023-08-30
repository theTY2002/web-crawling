#input: zte urls
#output: downloads PDFs

from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup

from tqdm import tqdm
from functions import *

import zipfile

NUM_PAGES = 10
BASE_URL = "https://www.zte.com.cn/"
articleLinks = []
zipList = []

def getLinksFromSoup(soup : BeautifulSoup) -> list[str]:
    """Get article links from BeautifulSoup object

    Args:
        soup (BeautifulSoup): BeautifulSoup object

    Returns:
        list[str]: List of article links
    """    
    articleLinks = []
    # finding links to HTML articles
    for a in soup.find_all("a", href = True):
        if ("/content/zte-site/www-zte-com-cn/china/about/magazine/zte-communications/2" in a['href']):
            articleLink = BASE_URL + a['href']
            articleLinks.append(articleLink)
    return articleLinks

def getLinksFromURL(url : str) -> list[str]:
    """Gets zip links from URL

    Args:
        url (str): ZTE url

    Returns:
        list[str]: list of zip links
    """    
    zipList = []
    # Send GET request
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('a', id = "maincontent_0_linkDetailZIP"):
        link = a['href'][1:]
        # print("Found the URL:", link)
        zipList.append(BASE_URL + link)
    return zipList

### Main

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
service = Service()
driver = webdriver.Chrome(service=service, options=options)


for i in range(1, NUM_PAGES + 1):
    print("page: " + str(i) + "/" + str(NUM_PAGES))
    driver.get("https://www.zte.com.cn/china/about/magazine/zte-communications.html?page=" + str(i))
    page_source = driver.page_source
    contentsSoup = BeautifulSoup(page_source, 'lxml')
    count = 0
    while True:
        print("attempt: " + str(count))
        count += 1
        if (len(getLinksFromSoup(contentsSoup)) == 0):
            driver.get("https://www.zte.com.cn/china/about/magazine/zte-communications.html?page=" + str(i))
            page_source = driver.page_source
            contentsSoup = BeautifulSoup(page_source, 'lxml')
        else:
            articleLinks.extend(getLinksFromSoup(contentsSoup))
            break

print(len(articleLinks))
print(articleLinks)

linkCount = 0
for link in articleLinks:
    print("link: " + str(linkCount) + "/" + str(len(articleLinks)))
    tempLinks = getLinksFromURL(link)
    zipList.extend(tempLinks)
    linkCount += 1
# print(zipList)

downloadCount = 0
for zipLink in zipList:
    print("downloads: " + str(downloadCount) + "/" + str(len(zipList)))
    # Send GET request
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(zipLink, headers=headers, timeout=60)
    download_pdf(zipLink, "downloads/zte/zte" + str(downloadCount) + ".zip")
    downloadCount += 1