#input: sciengine URLs
#output: json files

from functions import *
import ctypes
from tqdm import *

start_time = time.time()

DEBUG = True
BASE_URL = "https://www.sciengine.com/SSI/issue/"
START_VOLUME = 41
END_VOLUME = 54
NUM_SECTIONS = 13 # number of processes
articleLinks = []
articleCount = multiprocessing.Value(ctypes.c_int, 0)  # (type, init value)
processList = []

def getLinksFromSoup(soup : BeautifulSoup) -> list[str]:
    """Gets article links from BeautifulSoup object

    Args:
        soup (str): BeautifulSoup object

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



def getArticleLinks(startVolume : int, endVolume : int, name : str, articleCount : int):
    """Get article links from existing section of list

    Args:
        startVolume (int): _description_
        endVolume (int): _description_
        name (str): _description_
        articleCount (int): _description_
    """    
    humanReadable = []
    # loop through links
    for volumeNum in trange(startVolume, endVolume):
        print("\n" + name + "volume: " + str(volumeNum) + "/" + str(endVolume - 1))
        END_ISSUE = 12
        # divide volumes
        if (volumeNum == 53): END_ISSUE = 7
        for issueNum in trange(1, END_ISSUE + 1):
            
            print("\n" + name + "issue: " + str(issueNum) + "/" + str(END_ISSUE))
            pageLink = BASE_URL + str(volumeNum) + "/" + str(issueNum)
            #if (DEBUG): print("pageLink: " + pageLink)
            pageSoup = URLtoSoup(pageLink)
            articleLinks = (getLinksFromSoup(pageSoup))
            articleCount.value += len(articleLinks)
            # print(name + str(articleCount.value))
            list2json(articleLinks, "sciEngineCNmultiarticleLinks.json")
            count = 1
            articleLinks = tqdm(articleLinks)
            for articleLink in articleLinks:
                if (DEBUG): print("\n" + name + "article: " + str(count) + "/" + str(len(articleLinks)))
                count += 1
                articleSoup = URLtoSoup(articleLink)
                textList = articleSoup.find_all("p")
                #print(textList)

                for aTag in textList:
                    soup = aTag
                    rawText = soup.get_text().strip()
                    humanReadable.append(rawText)
    
    list2json(humanReadable, "sciEngineCNmulti" + name[:-2] + ".json")

# Main

if __name__ == "__main__":
    totalSize = END_VOLUME - START_VOLUME
    remainder = totalSize % NUM_SECTIONS
    sectionSize = (totalSize - remainder) // NUM_SECTIONS
    # for each process
    for sectionIndex in range(0, NUM_SECTIONS):
        startOffset = sectionSize * sectionIndex
        endOffset = sectionSize * (sectionIndex + 1)
        name = "P" + str(sectionIndex) + ": "
        print("startVolume: " + str(START_VOLUME + startOffset))
        print("endVolume: " + str(START_VOLUME + endOffset))
        if (sectionIndex != (NUM_SECTIONS - 1)):
            process = multiprocessing.Process(target=getArticleLinks, args=(START_VOLUME + startOffset, START_VOLUME + endOffset, name, articleCount))
        else:
            process = multiprocessing.Process(target=getArticleLinks, args=(START_VOLUME + startOffset, START_VOLUME + endOffset + remainder, name, articleCount))
        processList.append(process)

    for process in processList:
        process.start()

    for process in processList:
        process.join()


# if (DEBUG): print("1st element: " + humanReadable[0])
# if (DEBUG): print("last element: " + humanReadable[-1])

    print("articleCount:" + str(articleCount.value))
    print("--- %s seconds ---" % (time.time() - start_time))