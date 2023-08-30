### Outdated/test file


#input: URLs
#output: json files
import re
from functions import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def htmlDownload(DEBUG : bool, BASE_URL : str):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    articleLinks = []
    START_PAGE = 2018
    END_PAGE = 2018 # 2023
    articleCount = 0


    def getLinksFromSoup(soup):
        articleLinks = []
        # finding links to HTML articles
        for a in soup.find_all("a", target="_blank"):
            articleLink = "https:" + a["href"]
            articleLinks.append(articleLink)
            print(articleLink)

        return articleLinks

    humanReadable = []
    for num in range(START_PAGE, END_PAGE + 1):
        if (DEBUG): print("page: " + str(num) + "/" + str(END_PAGE))
        minIssue = 8
        maxIssue = 13
        if (num == 2018): minIssue = 8
        if (num == 2023): maxIssue = 7
        # issue number
        for issueNum in range (minIssue, maxIssue):
            if (DEBUG): print("issue: " + str(issueNum) + "/" + str(maxIssue))
            pageURL = BASE_URL + str(num) + "/" + str(issueNum)
            if (DEBUG): print("pageURL: " + pageURL)
            attempts = 0
            while True:
                print("attempt: " + str(attempts))
                attempts += 1
                if (len(articleLinks) == 0):
                    #time.sleep(random.randint(2, 5))
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