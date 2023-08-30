from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup

def downloadZip(zipurl : str):    
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall('/Users/trevor/VSCode/downloads')


def getLinksFromURL(url):
    zipList = []

    # Making a GET request
    r = requests.get(url)

    # check status code for response received
    # success code - 200
    print(r)

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('a', href=True):
        link = a['href']
        print("Found the URL:", link)
        if(link.endswith('.zip')):
            zipList.append(link)
            

    print(zipList)

import docx2txt

# extract text
text = docx2txt.process('downloads/29503_CR1032_(Rel-18)_C4-231087 CR 29503-i10 multiple data set retrieval with query parameters.docx')

# convert to list
li = [x for x in text.split('\n')]
# remove ''s i.e Nones
li = list(filter(None, li))

for text in li:
    li[li.index(text)] = text.strip()

print(li)