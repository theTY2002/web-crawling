###Outclassed by more efficient multiprocessing function; depreceated

#input: sciengine URLs
#output: json files

from functions import *
import time

start_time = time.time()
DEBUG = True
BASE_URL = "https://www.sciengine.com/SSI/issue/"
START_VOLUME = 41
END_VOLUME = 42 #53
articleLinks = []
articleCount = 0

def getLinksFromSoup(soup : BeautifulSoup) -> list[str]:
    """ Gets links from Beauifuloup object

    Args:
        soup (BeautifulSoup): BeautifulSoup object

    Returns:
        list[str]: list of article links
    """    
    articleLinks = []
    # finding links to HTML articles
    for a in soup.find_all("a", target="_blank"):
        #print(a)
        if (a["href"].startswith("https://doi.org")):
            articleLink = a["href"]
            articleLinks.append(articleLink)
            #print(articleLink)
    return articleLinks

### Main
humanReadable = []
page = 1
# loop through links
for volumeNum in range(START_VOLUME, END_VOLUME + 1):
    print("volume: " + str(volumeNum) + "/" + str(END_VOLUME))
    page += 1
    END_ISSUE = 12
    if (volumeNum == 53): END_ISSUE = 7
    for issueNum in range(1, 2):#END_ISSUE + 1):
        print("issue: " + str(issueNum) + "/" + str(END_ISSUE))
        pageLink = BASE_URL + str(volumeNum) + "/" + str(issueNum)
        #if (DEBUG): print("pageLink: " + pageLink)
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
            
            break


# if (DEBUG): print("1st element: " + humanReadable[0])
# if (DEBUG): print("last element: " + humanReadable[-1])

print("articleCount:" + str(articleCount))
print("--- %s seconds ---" % (time.time() - start_time))
list2json(humanReadable, "sciEngineCN.json")