#input: caict URLs
#output: downloads PDFs

from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup

from tqdm import tqdm
import zipfile
from functions import *
import time

NUMPAGES = 17
zipList = []
pdfList = []

def pwd(url : str) -> str:
    """Returns the substring of the URL before the last occurence of the "/" character

    Args:
        url (str): URL

    Returns:
        str: substring of URL
    """    
    lastSlashIndex = url.rfind("/")
    return url[0:lastSlashIndex]

def getLinksFromURL(url : str):
    """Gets links of PDFs from website and adds them to list

    Args:
        url (str): URL of caict website
    """    
    # Making a GET request
    r = requests.get(url)
    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    #find and append all PDF links
    for a in soup.find_all('a', href=True):
        link = a['href'][1:]
        if(link.endswith('.pdf')):
            pdfList.append(pwd(url) + link)

def downloadZip(zipurl : str):
    """Downloads zip files from URL

    Args:
        zipurl (str): URL of zip file
    """    
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read()), metadata_encoding = "utf-8") as zfile:
            print(zfile.infolist())
            for member in tqdm(zfile.infolist(), desc='Extracting '):
                try:
                    zfile.extract(member, 'downloads')
                except zipfile.error as e:
                    pass

### Main

currPageURL = ""
# for each page:
for i in range(0, NUMPAGES):
    print("page: " + str(i) + "/" + str(NUMPAGES - 1))
    if (i == 0):
        currPageURL = "http://www.caict.ac.cn/kxyj/qwfb/bps/index.htm"
    else:
        currPageURL = "http://www.caict.ac.cn/kxyj/qwfb/bps/index_" + str(i) + ".htm"

    # attempt requests until successful
    while True:
        try:
            # Making a GET request
            r = requests.get(currPageURL, timeout=60)
            break
        except requests.exceptions.Timeout as err:
            print(err)
            time.sleep(3)

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find all article links
    articleList = soup.find_all("td", width = "540")
    
    # For each article link
    for article in articleList:
        link = article.find("a")
        link = link["href"][1:]
        # print(link)
        articleURL = pwd(currPageURL) + link
        # print(articleURL)
        getLinksFromURL(articleURL)


count = 0
#for pdfURL in pdfList:
for i in range(0, len(pdfList)):
    pdfURL = pdfList[i]
    print(str(i) + "/" + str(len(pdfList) - 1))
    # Define URL of a PDF
    url = pdfURL

    # Define PDF file name
    file_name = "downloads/caict/caict" + str(i - 1) + ".pdf"

    # Download PDF
    download_pdf(url, file_name)
    count += 1