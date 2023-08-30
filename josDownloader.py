#input: jos URLs
#output: json files

from functions import *

DEBUG = True
BASE_URL = "https://www.jos.org.cn/"
articleLinks = []
START_YEAR = 2023
END_YEAR = 2023 #2023
indexList = ["s1", "s2"]
articleCount = 0

def getLinksFromSoup(soup : str) -> list[str]:
    """Gets links from BeautifulSoup object

    Args:
        soup (str): BeautifulSoup object

    Returns:
        list[str]: list of article links
    """    
    articleLinks = []
    # finding links to HTML articles
    for a in soup.find_all("a", class_="btn_html", target="_blank"):
        #print(a)
        articleLink = a["href"]
        articleLinks.append("https://www.jos.org.cn/" + articleLink)
        #print("https://www.jos.org.cn/" + articleLink)
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


#### Main
humanReadable = []
pageLinks = []
page = 1
# loop through links
for year in range(START_YEAR, END_YEAR + 1):
    print("year: " + str(year) + "/" + str(END_YEAR))
    page += 1
    volumeNum = year - 1989
    for issueNum in range(1, 15):
        print("issue: " + str(issueNum) + "/" + str(14))
        if (issueNum <= 12):
            pageLink = "https://www.jos.org.cn/jos/article/issue/" + str(year) + "_" + str(volumeNum) + "_" + str(issueNum)
        else:
            pageLink = "https://www.jos.org.cn/jos/article/issue/" + str(year) + "_" + str(volumeNum) + "_s" + str(issueNum - 12)
        #if (DEBUG): print("pageLink: " + pageLink)
        pageSoup = URLtoSoup(pageLink)
        articleLinks = getLinksFromSoup(pageSoup)
        articleCount += len(articleLinks)
        count = 1
        for articleLink in articleLinks:
            if (DEBUG): print("article: " + str(count) + "/" + str(len(articleLinks)))
            #if (DEBUG): print("articleLink: " + articleLink)
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

print("articleCount: " + str(articleCount))

list2json(humanReadable, "jos2023.json")