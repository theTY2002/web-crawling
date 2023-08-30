#input: ictp URLs
#output: json files

import re
from functions import *

DEBUG = True
BASE_URL = "http://ictp.caict.ac.cn/"
articleLinks = []
START_PAGE = 44
END_PAGE = 60
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
    for a in soup.find_all("a", class_="html"):
        articleIndex = a['onclick'].find("article")
        if (articleIndex != -1):
            articleLink = a['onclick'][articleIndex:len(a['onclick']) - 16]
            articleLinks.append(BASE_URL + articleLink)
            # print(articleLink)
    return articleLinks

### Main

humanReadable = []
for num in range(START_PAGE, END_PAGE + 1):
    if (DEBUG): print("page: " + str(num) + "/" + str(END_PAGE))
    pageURL = "http://ictp.caict.ac.cn/CN/volumn/volumn_"+ str(num) + ".shtml"
    if (DEBUG): print("pageURL: " + pageURL)
    contentsSoup = URLtoSoup(pageURL)
    articleLinks = getLinksFromSoup(contentsSoup)
    if (DEBUG): print("articleLinks length: " + str(len(articleLinks)))
    articleCount += len(articleLinks)
    count = 0
    for articleLink in articleLinks:
        if (DEBUG): print("article: " + str(count) + "/" + str(len(articleLinks) - 1))
        count += 1
        articleSoup = URLtoSoup(articleLink)
        regex = re.compile("[C][0-9]+")
        #print(regex)
        textList = articleSoup.find_all("p", id=regex)
        #print(textList)

        if (len(textList) == 0):
            regex = re.compile("p[0-9]+")
            #print(regex)
            textList = articleSoup.find_all("p", id=regex)

        for aTag in textList:
            soup = aTag
            rawText = soup.get_text().strip()
            if "\\" in rawText or "≈" in rawText or "{" in rawText or "}" in rawText:
                continue
            humanReadable.append(soup.get_text().strip())

if (DEBUG): print("1st element: " + humanReadable[0])
if (DEBUG): print("last element: " + humanReadable[-1])

print(articleCount)

list2json(humanReadable, "ictp.json")