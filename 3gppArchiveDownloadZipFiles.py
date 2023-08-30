#reads txt file of zip links, downloads zip files
#output: downloads zip files

import wget
from functions import *
import multiprocessing
import time
from tqdm import *
import sys

start_time = time.time()
NUM_SECTIONS = 5
processList = []
INPUT_FILE = "3gppArchiveZipLinksTEST.txt"

def pwd(url : str) -> str:
    """Returns the substring of the URL after the last occurence of the "/" character

    Args:
        url (str): URL

    Returns:
        str: substring of URL
    """    
    lastSlashIndex = url.rfind("/")
    return url[lastSlashIndex + 1:]

def downloadZip(zipURL : str):
    """Downloads zip file from URL

    Args:
        zipURL (str): URL of zip file
    """    
    
    filename = pwd(zipURL)
    # filename = filename[31:]
    outputPath = "3gppArchiveZip/" + filename

    # save URL if unable to download
    try:
        wget.download(zipURL,out = outputPath)
    except:
        original_stdout = sys.stdout
        with open('offendingLinks.txt', 'a') as f:
            sys.stdout = f # Change the standard output to the file we created.
            print("offending URL:" + zipURL + "\n")
            sys.stdout = original_stdout

def downloadFromList(linksList : list, startIndex : int, endIndex : int, name : str):
    """Calls downloadZip(), downloads multiple zip files from a section of a list of URLs

    Args:
        linksList (list): List containing URLs of .zip files
        startIndex (int): Starting index of section (in list)
        endIndex (int): Ending index of section (in list)
        name (str): Process name
    """    
    
    # Loops through a section of links
    for i in trange(startIndex, endIndex):
        print("\n" + name + ": " + str(i) + "/" + str(endIndex))
        downloadZip(linksList[i])

    # prints finish time of each process
    original_stdout = sys.stdout
    with open('finishTime.txt', 'a') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print(name + ": ")
        print("--- %s seconds ---" % (time.time() - start_time))
        sys.stdout = original_stdout

def getLinks(URL : str, endsWith : str):
    soup = URLtoSoup(URL)

    aLinks = soup.find_all("a")
    links = []
    for link in aLinks:
        if link["href"].endswith(endsWith):
            links.append(link["href"])
    #print(links)
    return links

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        zipLinksList = [x.rstrip() for x in f]
        print("zipLinksList: " + str(zipLinksList))

    totalSize = len(zipLinksList)
    remainder = totalSize % NUM_SECTIONS
    sectionSize = (totalSize - remainder) // NUM_SECTIONS

    for sectionIndex in range(0, NUM_SECTIONS):
        startOffset = sectionSize * sectionIndex
        endOffset = sectionSize * (sectionIndex + 1)
        name = "P" + str(sectionIndex)
        print("startOffset: " + str(startOffset))
        print("endOffset: " + str(endOffset))
        if (sectionIndex != (NUM_SECTIONS - 1)):
            process = multiprocessing.Process(target=downloadFromList, args=(zipLinksList, startOffset, endOffset, name))
        else:
            process = multiprocessing.Process(target=downloadFromList, args=(zipLinksList, startOffset, endOffset + remainder, name))
        processList.append(process)

    for process in processList:
        process.start()

    for process in processList:
        process.join()

    print("--- %s seconds ---" % (time.time() - start_time))