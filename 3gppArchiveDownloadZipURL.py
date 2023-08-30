#writes all zipfile URLs to txt from 3gpp in spec Archive
#output: list of txts

from functions import *
import multiprocessing
import time
import ctypes
from tqdm import *
import sys
import ctypes

start_time = time.time()
NUM_SECTIONS = 20
articleCount = multiprocessing.Value(ctypes.c_int, 0)

def pwd(url : str) -> int:
    """Returns the substring of the URL after the last occurence of the "/" character

    Args:
        url (str): URL

    Returns:
        str: substring of URL
    """    
    lastSlashIndex = url.rfind("/")
    return url[lastSlashIndex + 1:]

def downloadZip(zipURL : str, articleCount : int):
    """Writes URL of zip file to specified .txt file

    Args:
        zipURL (str): URL of .zip file
        articleCount (int): current number of articles processed
    """    
    
    #process filename
    filename = re.sub("/", "-", zipURL)
    filename = filename[31:]
    
    #writes URL to file
    original_stdout = sys.stdout
    with open('3gppArchiveZipLinks.txt', 'a') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print(zipURL)
        sys.stdout = original_stdout

    #Increment article count
    articleCount.value += 1


def getLinks(URL : str, endsWith : str) -> list[str]:
    """Get links that end with the desired suffix from 3gpp website

    Args:
        URL (str): URL of 3gpp website
        endsWith (str): desired suffix

    Returns:
        list[str]: list of links
    """    
    soup = URLtoSoup(URL)

    aLinks = soup.find_all("a")
    links = []
    for link in aLinks:
        if link["href"].endswith(endsWith):
            links.append(link["href"])
    #print(links)
    return links

def getLinksStartsWith(URL : str, startsWith : str) -> list[str]:
    """Get links that end with the desired suffix from 3gpp website

    Args:
        URL (str): URL of 3gpp website
        endsWith (str): desired suffix

    Returns:
        list[str]: list of links
    """    
    soup = URLtoSoup(URL)

    aLinks = soup.find_all("a")
    links = []
    for link in aLinks:
        linkString = link.get_text().strip()
        if linkString.startswith(startsWith):
            links.append(link["href"])
    #print(links)
    return links

def getZipLinks(uLinks : list[str], startIndex : int, endIndex : int, name : str):

    for i in trange(startIndex, endIndex):
        uLink = uLinks[i]
        zipLinks = getLinks(uLink, ".zip")
        for zipLink in zipLinks:
            downloadZip(zipLink, articleCount)
        print("\n" + name + ": " + str(i) + "/" + str(endIndex))

    # print("\n" + name)
    # seriesIndex = 0
    # seriesLinks = getLinks(currURL, "series")
    # for seriesURL in tqdm(seriesLinks):
    #     seriesIndex += 1
    #     zipLinks = getLinks(seriesURL, ".zip")
    #     #print(zipLinks)
    #     zipIndex = 0
    #     for zipLink in zipLinks:
    #         zipIndex += 1
    #         downloadZip(zipLink, articleCount)
    #         print("\n" + name + "series: " + str(seriesIndex) + "/" + str(len(seriesLinks)) + "  zip: " + str(zipIndex) + "/" + str(len(zipLinks)))

BASE_URL = "https://www.3gpp.org/ftp/Specs/archive"
# specsDirectories = ["2022-12", "2023-03", "2023-06"] #do archive later separately

if __name__ == "__main__":
    seriesDirectories = getLinks(BASE_URL, "_series")

    processList = []
    uLinks = []
    for seriesURL in tqdm(seriesDirectories):
        #get U URLs that start with the series number
        
        uLinks.extend(getLinksStartsWith(seriesURL, pwd(seriesURL)[0:2]))
        #print(uLinks)
        
        
        #break #comment out later pls
        
        
    print(uLinks)

    totalSize = len(uLinks)
    print("totalSize: " + str(totalSize))
    remainder = totalSize % NUM_SECTIONS
    sectionSize = (totalSize - remainder) // NUM_SECTIONS

    # getZipLinks(uLinks, 0, len(uLinks), "Hi")

    for sectionIndex in range(0, NUM_SECTIONS):
        startOffset = sectionSize * sectionIndex
        endOffset = sectionSize * (sectionIndex + 1)
        name = "P" + str(sectionIndex)
        print("startOffset: " + str(startOffset))
        print("endOffset: " + str(endOffset))
        if (sectionIndex != (NUM_SECTIONS - 1)):
            process = multiprocessing.Process(target=getZipLinks, args=(uLinks, startOffset, endOffset, name))
        else:
            process = multiprocessing.Process(target=getZipLinks, args=(uLinks, startOffset, endOffset + remainder, name))
        processList.append(process)

    for process in processList:
        process.start()

    for process in processList:
        process.join()

    print("articleCount:" + str(articleCount.value))
    print("--- %s seconds ---" % (time.time() - start_time))