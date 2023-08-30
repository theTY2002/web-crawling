#input: bupt URLs
#output: json files

from functions import *

DEBUG = True
BASE_URL = "https://journal.bupt.edu.cn/CN/article/showTenYearVolumnDetail.do?nian="
articleLinks = []
START_YEAR = 2013
END_YEAR = 2022
articleCount = 0

def getLinksFromSoup(soup):
    articleLinks = []
    # finding links to HTML articles
    for a in soup.find_all("a", class_="html"):
        ### This website's HTML links are formatted in 2 different ways across time, if-else catches both formats
        if (a["href"] == "#"):
            articleIndex = a['onclick'].find("article")
            if (articleIndex != -1):
                articleLink = a['onclick'][articleIndex:len(a['onclick']) - 16]
                articleLinks.append("https://journal.bupt.edu.cn/" + articleLink)
            print(articleLink)
        else:
            articleLink = a["href"]
            #print(articleLink)
            articleLinks.append(articleLink)

    return articleLinks


def getPageLinksFromSoup(soup) -> list[str]:
    """Gets and returns list of page links from BeautifulSoup object

    Args:
        soup (_type_): BeautifulSoup object

    Returns:
        list[str]: list of page links
    """    
    pageLinks = []
    for td in soup.find_all("td", height = 20, class_="J_WenZhang"):
        for link in td.find_all("a", class_="J_WenZhang"):
            pageLink = "https://journal.bupt.edu.cn/CN" + link['href'][2:]
            pageLinks.append(pageLink)
            #print(pageLink)
    return pageLinks


### Main

humanReadable = []
#for each year:
for num in range(START_YEAR, END_YEAR + 1):
    if (DEBUG): print("year: " + str(num) + "/" + str(END_YEAR))
    yearURL = BASE_URL + str(num)
    if (DEBUG): print("yearURL: " + yearURL)
    contentsSoup = URLtoSoup(yearURL)
    pageLinks = getPageLinksFromSoup(contentsSoup)
    if (DEBUG): print("pageLinks length: " + str(len(pageLinks)))
    page = 1
    #for each page in a year:
    for pageLink in pageLinks:
        print("page: " + str(page) + "/" + str(len(pageLinks)))
        page += 1
        pageSoup = URLtoSoup(pageLink)
        articleLinks = getLinksFromSoup(pageSoup)
        articleCount += len(articleLinks)
        count = 0
        # for each article in a page:
        for articleLink in articleLinks:
            if (DEBUG): print("article: " + str(count) + "/" + str(len(articleLinks) - 1))
            count += 1
            articleSoup = URLtoSoup(articleLink)
            textList = articleSoup.find_all("p")
            #print(textList)
            # for each piece of text in an article
            for aTag in textList:
                soup = aTag
                rawText = soup.get_text().strip()
                humanReadable.append(soup.get_text().strip())


if (DEBUG): print("1st element: " + humanReadable[0])
if (DEBUG): print("last element: " + humanReadable[-1])

print("articleCount:" + str(articleCount))

#convert final list into JSON file
list2json(humanReadable, "bupt.json")