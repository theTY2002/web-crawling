#writes all zipfile URLs to txt from 3gpp in specs 2022-12, 2023-03, 2023-06
#output: list of txts

from functions import *
import multiprocessing
import time
import ctypes
from tqdm import *
import sys
import ctypes

start_time = time.time()
articleCount = multiprocessing.Value(ctypes.c_int, 0)

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
    with open('3gppZipLinks.txt', 'a') as f:
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

def getZipLinks(currURL : str, name : str, articleCount):
    """Navigates the website structure of 3gpp, getting links of .zip files and calling downloadZip()

    Args:
        currURL (str): URL of 3gpp website
        name (str): Name of process
        articleCount (_type_): Current article count
    """    
    print("\n" + name)
    seriesIndex = 0
    seriesLinks = getLinks(currURL, "series")
    for seriesURL in tqdm(seriesLinks):
        seriesIndex += 1
        zipLinks = getLinks(seriesURL, ".zip")
        #print(zipLinks)
        zipIndex = 0
        for zipLink in zipLinks:
            zipIndex += 1
            downloadZip(zipLink, articleCount)
            print("\n" + name + "series: " + str(seriesIndex) + "/" + str(len(seriesLinks)) + "  zip: " + str(zipIndex) + "/" + str(len(zipLinks)))

BASE_URL = "https://www.3gpp.org/ftp/Specs/"
specsDirectories = ["2022-12", "2023-03", "2023-06"] #do archive later separately

if __name__ == "__main__":
    relDirectories = []
    for i in range(8, 20):
        relDirectories.append("Rel-" + str(i))

    for specsURL in specsDirectories:
        # print("SPEC " + specsURL + " START")
        processList = []
        for relURL in relDirectories:
            currDir = specsURL + "/" + relURL
            currURL = BASE_URL + currDir
            name = "P" + relURL + ": "
            process = multiprocessing.Process(target=getZipLinks, args=(currURL, name, articleCount))
            processList.append(process)

        for process in processList:
            process.start()

        for process in processList:
            process.join()

    print("articleCount:" + str(articleCount.value))
    print("--- %s seconds ---" % (time.time() - start_time))