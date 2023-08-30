#input: dlxxtx URLs
#output: json files

import re
from functions import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
service = Service()
driver = webdriver.Chrome(service=service, options=options)

DEBUG = True
BASE_URL = "http://www.dlxxtx.com/CN/"
articleLinks = []
START_PAGE = 2021
END_PAGE = 2023
articleCount = 0


def getLinksFromSoup(soup : BeautifulSoup) -> list[str]:
    """Gets article links from BeautifulSoup object

    Args:
        soup (BeautifulSoup): BeautifulSoup object

    Returns:
        list[str]: list of article links
    """    
    articleLinks = []
    # finding links to HTML articles
    for a in soup.find_all("a", class_="j-html"):
        articleLink = a["href"]
        articleLinks.append(articleLink)
        #print(articleLink)
    return articleLinks

### Main
humanReadable = []
for num in range(START_PAGE, END_PAGE + 1):
    if (DEBUG): print("page: " + str(num) + "/" + str(END_PAGE))
    maxIssue = 13
    if (num == 2023): maxIssue = 8
    # issue number
    for i in range (1, maxIssue):
        if (DEBUG): print("issue: " + str(i) + "/" + str(12))
        pageURL = BASE_URL + "Y" + str(num) + "/V" + str(num - 2002) + "/I" + str(i)
        if (DEBUG): print("pageURL: " + pageURL)
        if (DEBUG): print("articleLinks length: " + str(len(articleLinks)))
        attempts = 0
        while True:
            print("attempt: " + str(attempts))
            attempts += 1
            if (len(articleLinks) == 0):
                contentsSoup = URLtoSoup(pageURL)
                articleLinks = getLinksFromSoup(contentsSoup)
            else:
                break
        articleCount += len(articleLinks)
        count = 1
        for articleLink in articleLinks:
            if (DEBUG): print("article: " + str(count) + "/" + str(len(articleLinks)))
            count += 1
            articleSoup = URLtoSoup(articleLink)
            regex = re.compile("[C][0-9]+")
            #print(regex)
            textList = articleSoup.find_all("p")
            #print(textList)

            for aTag in textList:
                soup = aTag
                rawText = soup.get_text().strip()
                if "\\" in rawText or "≈" in rawText or "{" in rawText or "}" in rawText:
                    continue
                humanReadable.append(soup.get_text().strip())

if (DEBUG): print("1st element: " + humanReadable[0])
if (DEBUG): print("last element: " + humanReadable[-1])

print("articleCount: " + str(articleCount))

list2json(humanReadable, "dlxxtx.json")