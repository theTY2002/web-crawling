#input: dlxxtx URLs
#output: json files

import re
from functions import *

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
service = Service()
driver = webdriver.Chrome(service=service, options=options)

DEBUG = True
BASE_URL = "https://jeit.ac.cn/article/"
articleLinks = []
START_PAGE = 2023
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
    for a in soup.find_all("a", target="_blank"):
        if (a["href"].endswith("viewType=HTML")):
            articleLink = "https:" + a["href"]
            articleLinks.append(articleLink)
            # print(articleLink)
    return articleLinks

### Main

humanReadable = []
for num in range(START_PAGE, END_PAGE + 1):
    if (DEBUG): print("page: " + str(num) + "/" + str(END_PAGE))
    minIssue = 1
    maxIssue = 13
    # issue where articles start to have HTML format
    if (num == 2018): minIssue = 8
    # issues have been published up to this point in 2023 (at the time of writing)
    if (num == 2023): maxIssue = 7

    # loop through issue number
    for issueNum in range (minIssue, maxIssue):
        if (DEBUG): print("issue: " + str(issueNum) + "/" + str(maxIssue - 1))
        pageURL = BASE_URL + str(num) + "/" + str(issueNum)
        if (DEBUG): print("pageURL: " + pageURL)
        attempts = 0
        # attempt conversion from URL to list of strings
        while True:
            print("attempt: " + str(attempts))
            if (len(articleLinks) == 0):
                contentsSoup = URLtoSoup(pageURL)
                articleLinks = getLinksFromSoup(contentsSoup)
                attempts += 1
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

            # append text to list
            for aTag in textList:
                soup = aTag
                rawText = soup.get_text().strip()
                if "\\" in rawText or "≈" in rawText or "{" in rawText or "}" in rawText:
                    continue
                humanReadable.append(soup.get_text().strip())

#print 1st and last element to verify accuracy of converted data
if (DEBUG): print("1st element: " + humanReadable[0])
if (DEBUG): print("last element: " + humanReadable[-1])

print("articleCount: " + str(articleCount))

list2json(humanReadable, "jeit2023.json")