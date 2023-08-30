#input: xidian URLs
#output: json files

from functions import *

DEBUG = True
BASE_URL = "https://journal.xidian.edu.cn/xdxb/CN/article/showOldVolumn.do"
articleLinks = []
START_YEAR = 2013
END_YEAR = 2022
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
    for a in soup.find_all("a", class_="txt_zhaiyao1"):
        #print(a)
        if (a["href"] == "#"):
            articleIndex = a['onclick'].find("article")
            if (articleIndex != -1):
                articleLink = a['onclick'][articleIndex:len(a['onclick']) - 16]
                articleLinks.append("https://journal.xidian.edu.cn/xdxb/" + articleLink)
            #print("https://journal.xidian.edu.cn/xdxb/" + articleLink)
    return articleLinks


def getPageLinksFromSoup(soup : BeautifulSoup) -> list[str]:
    """Gets page links from BeautifulSoup object

    Args:
        soup (BeautifulSoup): BeautifulSoup object

    Returns:
        list[str]: list of page links
    """    
    pageLinks = []
    for td in soup.find_all("td"):
        for link in td.find_all("a"):
            pageLink = "https://journal.xidian.edu.cn/xdxb/CN" + link['href'][2:]
            pageLinks.append(pageLink)
    return pageLinks

### Main

archiveSoup = URLtoSoup("https://journal.xidian.edu.cn/xdxb/CN/article/showOldVolumn.do")
pageLinks = getPageLinksFromSoup(archiveSoup)

#filter articles, only take articles >= 2019
goodLinks = []
#get number from end of link
for pageLink in pageLinks:
    numSubstring = pageLink[-10:-6]
    #print(numSubstring)
    articleNum = int(numSubstring)
    #if article is from >= 2019
    if (articleNum >= 1388):
        goodLinks.append(pageLink)

goodLinks = list(dict.fromkeys(goodLinks))
# print(goodLinks)

humanReadable = []
page = 1
for goodLink in goodLinks:
    print("page: " + str(page) + "/" + str(len(goodLinks)))
    page += 1
    pageSoup = URLtoSoup(goodLink)
    articleLinks = getLinksFromSoup(pageSoup)
    articleCount += len(articleLinks)
    count = 1
    for articleLink in articleLinks:
        if (DEBUG): print("article: " + str(count) + "/" + str(len(articleLinks) - 1))
        count += 1
        articleSoup = URLtoSoup(articleLink)
        textList = articleSoup.find_all("p")
        #print(textList)

        for aTag in textList:
            soup = aTag
            rawText = soup.get_text().strip()
            humanReadable.append(soup.get_text().strip())


if (DEBUG): print("1st element: " + humanReadable[0])
if (DEBUG): print("last element: " + humanReadable[-1])

print("articleCount:" + str(articleCount))

list2json(humanReadable, "xidian.json")