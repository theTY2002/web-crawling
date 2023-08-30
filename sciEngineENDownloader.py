#input: sciengine URLs
#output: json files

from functions import *

DEBUG = True
BASE_URL = "https://www.sciengine.com/sands/issue/"
START_VOLUME = 1
END_VOLUME = 2
articleLinks = []
articleCount = 0

def getLinksFromSoup(soup):
    articleLinks = []
    # finding links to HTML articles
    for a in soup.find_all("a", target="_blank"):
        #print(a)
        if (a["href"].startswith("https://doi.org")):
            articleLink = a["href"]
            articleLinks.append(articleLink)
            print(articleLink)
    return articleLinks

humanReadable = []
pageLinks = []
page = 1
# loop through links
for volumeNum in range(START_VOLUME, END_VOLUME + 1):
    print("volume: " + str(volumeNum) + "/" + str(END_VOLUME))
    page += 1
    for issueNum in range(0, 1):
        print("issue: " + str(issueNum) + "/" + str(0))
        pageLink = BASE_URL + str(volumeNum) + "/" + str(issueNum)
        if (DEBUG): print("pageLink: " + pageLink)
        pageSoup = URLtoSoup(pageLink)
        articleLinks = getLinksFromSoup(pageSoup)
        articleCount += len(articleLinks)
        count = 1
        for articleLink in articleLinks:
            if (DEBUG): print("article: " + str(count) + "/" + str(len(articleLinks)))
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

list2json(humanReadable, "sciEngineEN.json")