### At the top level, webcrawling for the purposes of obtaining training data involves an input of URL & an ouput of .json file(s)

### In the functions.py file, I have written functions that can be shared across web crawling programs
### that crawl different websites. All functions that are not present in this file can be found in the functions.py file,
### as well as more detailed explanations of how they work
from functions import *

### Source websites typically have a multi-layered structure, where there is at least 1 "contents" page
### containing a list of all article links (there may be more).

### Sets the starting time
start_time = time.time()

### Depending on how the website is structured, the BASE_URL is usually the URL of the top-level "contents" page
BASE_URL = ""

### You will usually want some constants that signify the start and end of where you want to crawl,
### e.g. START_VOLUME, START_YEAR, START_PAGE, etc., depending on the specific structure of the website.
START_ = 0
END_ = 1

### If you choose to use multiprocessing, it is a good idea to set the number of sections that you want to partition
### your data into (and therefore the number of processes) as a constant in order for it to be easily changed.
### For maximum efficiency, choose a number that can evenly divide into the number of items that you plan to process,
### the highest advisable number depends on the processing power of your computer.
NUM_SECTIONS = 10

### Instantiation of articleLinks, a list where article links will be inserted
### It is a good idea to retrieve all links first, then process them to save time and/or prevent data loss.
### This list can also be saved to a local file in order to save time on repeat runs.
articleLinks = []

### Instantiation of articleCount, a counter for the number of articles 
### This is good for tracking the progress of your webcrawling, and to know where to continue in case of failure
### mid-way through the crawling process. If you choose to use multiprocessing, the value of this variable will likely
### be inaccurate due to race conditions between processes.
articleCount = 0

### Instantiation of processList, a list where processes will be inserted (if multiprocessing is used)
processList = []

### Unless the article URLs are sequential, you will need this function to extract all the links that are on a page.
### This function will look very similar for each website, but the identification method for the <a> tag will be slightly
### different, depending on the website that you are crawling
def getLinksFromSoup(soup : BeautifulSoup) -> list[str]:
    """Gets links from BeautifulSoup object

    Args:
        soup (str): BeautifulSoup object

    Returns:
        list[str]: list of article links
    """    
    articleLinks = []

    ### You can find the appropriate links in the page by giving specific attributes of tags as parameters in the find_all()
    ### function, more information can be found in the BeautifulSoup documentation
    for a in soup.find_all("a", target="_blank"):
        #print(a)

        ### Depending on the website, you may need to do additional filtering afterwards
        if (a["href"].startswith("https://doi.org")):
            articleLink = a["href"]
            articleLinks.append(articleLink)
            #print(articleLink)
    return articleLinks

### Typical steps of a webcrawler for a website with basic structure:
### Instantiate final list (to be turned into .json file)
### for each page in all pages:
###     get pageURL, convert to soup object using URLtoSoup
###     articleLinks = getLinksFromSoup(contentsSoup)
###     for each articleLink in articleLinks:
###         convert to soup object
###         filter paragraphs from soup object
###         append to final list
### Convert list to .json file
###
### For more details, please refer to ictpDownloader2022+.py which is a real code example.


### Typical steps of a webcrawler using multiprocessing:
### Enclose all the steps in the above section within 1 function, e.g. getArticleLinks()
### This function will take parameters of startIndex (int), endIndex (int), and name (str)
### if __name__ == "main":  # This line has to be included whenever multiprocessing is called/used/run in the main function
###     Calculate the size of sections depending on how many processes you want/need, e.g.:
###     totalSize = END_VOLUME - START_VOLUME
###     remainder = totalSize % NUM_SECTIONS
###     sectionSize = (totalSize - remainder) // NUM_SECTIONS
###     for each section:
###         Calculate start and end offsets of indices, e.g.:
###         startOffset = sectionSize * sectionIndex
###         endOffset = sectionSize * (sectionIndex + 1)
###         name = "P" + str(sectionIndex) + ": "   # Give each process a name for identification purposes
###         Create processes with appropriate parameters, e.g.:
###         if (sectionIndex != (NUM_SECTIONS - 1)):
###             process = multiprocessing.Process(target=getArticleLinks, args=(START_VOLUME + startOffset, START_VOLUME + endOffset, name, articleCount))
###         else:
###             process = multiprocessing.Process(target=getArticleLinks, args=(START_VOLUME + startOffset, START_VOLUME + endOffset + remainder, name, articleCount))
###         processList.append(process)
###         Start and join processes using for loops
###
### For more details, please refer to sciEngineCNDownloader multiprocess.py which is a real code example.
###
### *** Due to a Python bug (at the time or writing and probably in the future as well), you are unable to terminate
###     multiprocesses manually, they are only able to stop when the normal execution of the program ends ***


### After you generate your initial .json file(s), you should clean up junk data
### This can be done by first using jsonReadNClean() to clean, convert, and possibly combine the .json files,
### which will have an output of a list of strings. This list can then be fed into list2json() in order to obtain
### a cleaned json file. For more details, please refer to the actual functions in functions.py, as well as jsonReader.py
### for real code examples.