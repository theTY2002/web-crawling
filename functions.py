# The "requests" library is used to request a specific URL
import requests

# BeautifulSoup is the main library that does the actual web scraping
from bs4 import BeautifulSoup

### The multiprocessing library allows the crawling of multiple sections of your datasource at the same time.
### At the time of writing, there is a Python bug that makes it such that you cannot manually terminate your program if
### if it is a multiprocess one. I'll mention the specific implementation of this in more detail later.
import multiprocessing

### The tqdm library can graphically show your progress in any loop by using a progress bar.
from tqdm import *

### The time library can show the total elapsed time of your program and each process.
import time

### The re library is important for data cleaning, as it allows the use of regex to match patterns in text
import re

### The selenium library gets the contents of a webpage, and can also interact with elements on it, similar to a human
### user. It can also access javascript content, which is typically not available if you are exclusively using BeautifulSoup.
### *If you encounter a chromedriver version incompatibility error, update selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *

# The PdfReader library helps with conversion from PDF files to a text format
from PyPDF2 import PdfReader

import os

# The doc2txt library helps with conversion from docx files to a text format
import docx2txt

### The convert function from the doc2docx library converts .doc files to .docx files, but requires Microsoft Word to be
### installed on the machine; works on Windows and Mac
from doc2docx import convert

# The json library helps with the creation of .json files
import json

### This is usually used in tandem with getLinksFromSoup in each web scraper
def URLtoSoup(url : str) -> BeautifulSoup:
    """Converts the contents of a website into a BeautifulSoup object

    Args:
        url (str): URL of website

    Returns:
        BeautifulSoup: soup object
    """    
    # Driver setup
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument(f"--user-agent={my_user_agent}")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    # If exception occurs, try again
    while (True):
        try:
            driver.get(url)
            break
        except (TimeoutException, WebDriverException) as error:
            print(str(error.__class__.__name__) + ", try again")
            driver.quit()
            driver = webdriver.Chrome(service=service, options=options)
            continue
    pageSource = driver.page_source
    contentsSoup = BeautifulSoup(pageSource, 'lxml')

    # quite driver to refresh it
    driver.quit()
    return contentsSoup

### This function is usually used at the end of the web scraping process, when you want to convert all your text into
### a .json file. The format of this .json file is tailored for use in the LMFlow framework, modifications may need to
### be made for use with other frameworks
def list2json(list : list[str], filename : str):
    """Converts a list of strings into a JSON file with a specific format

    Args:
        list (list[str]): List of text
        filename (str): Output file path of the desired json file
    """    
    dictionary = {
        "type": "text_only",
        "instances": []
    }

    for element in list:
        pair = {"text" : element}
        dictionary["instances"].append(pair)

    jsonObject = json.dumps(dictionary, indent = 4, ensure_ascii = False)

    with open(filename, "w", encoding='utf-8') as outfile:
        outfile.write(jsonObject)


def pdf2Json(numRemoveFromStart : int, numRemoveFromEnd : int, inputFilePath : str, outputFilePath : str, toBeRemoved : list[str], regex : bool, mode : str):
    """Converts a PDF file into a JSON file of a specific format

    Args:
        numRemoveFromStart (int): Number of pages to omit from the start of the PDF
        numRemoveFromEnd (int): Number of pages to omit from the end of the PDF
        inputFilePath (str): Input file path of the PDF file
        outputFilePath (str): Output file path of the desired JSON file
        toBeRemoved (list[str]): List of strings that will be removed if in text
        regex (bool): unused/for a specific source
        mode (str): Data source that you can converting from
    """    
    dynamicItem = ""
    
    # creating a pdf reader object
    reader = PdfReader(inputFilePath)

    # printing number of pages in pdf file
    print(len(reader.pages))

    list = []

    #first X pages are removed (title, table of contents)
    for i in range (numRemoveFromStart, len(reader.pages) - numRemoveFromEnd):
        page = reader.pages[i]
        # extracting text from page
        text = page.extract_text()
        text = re.sub('\n', '', text)

        ### specific code written for specific datasources --------------
        if "\\" in text or "" in text or "" in text or "________________" in text or "···············" in text or "……………" in text or "......" in text:
            continue

        if (mode == "caict" and dynamicItem == ""):
            for item in toBeRemoved:
                res = re.search(item, text)
                if (res is not None):
                    dynamicItem = text[0:res.end() - 1].strip()
                    #print(dynamicItem)
        
        if (dynamicItem != ""):
            text = re.sub(dynamicItem, '', text)

        if regex:
            for item in toBeRemoved:
                res = re.search(item, text)
                if (res is not None):
                    text = text[res.end():]
        ### -------------------------------------------------------------

        ### skip pages that have characters that cause errors, this is here because some invalid characters can be written to
        ### .json file even though they cannot be printed
        try:
            print(text)
        except UnicodeEncodeError:
            continue

        text = text.strip()

        # remove empty lines
        if (text == ""):
            continue

        list.append(text)

    list2json(list, outputFilePath)

def download_pdf(url : str, file_name : str):
    """Downloads a PDF file from an online source

    Args:
        url (str): URL of PDF
        file_name (str): Output file path of desired PDF file
    """    

    # Send GET request
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    # Retry until successful
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=60)
        except requests.exceptions.ChunkedEncodingError or requests.exceptions.ConnectionError or TimeoutError:
            print("Timeout, try again")
            time.sleep(2)           

    # Save the PDF
        if response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(response.content)
            break
        else:
            print(response.status_code)
            time.sleep(2)
            continue

### Main function that cleans .json files
### Depending on the contents of your datasource, you can choose specific fragments of text to either skip or replace
### Regex can also be used to match specific patterns of text
def jsonReadNClean(filename : str, cutoffLen : int, source : str) -> list[str]:
    """Cleans json file, removing junk data

    Args:
        filename (str): Input file path of JSON file
        cutoffLen (int): The minimum length (number of characters) that a piece of text can be
        source (str): Data source

    Returns:
        list[str]: list of strings containing cleaned text
    """
    returnList = []
    title = ""

    # Opening JSON file
    f = open(filename)

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json list
    # print(len(data["instances"]))
    for i in trange(0, len(data["instances"])):
        text = data["instances"][i]["text"]

        # Skip empty text and text w/ symbols
        if (text == ""):
            continue
        if ("@" in text):
            continue
        if ("©" in text):
            continue
            
        # Replace invalid characters
        for char in text:
            if u'\u0000' <= char <= u'\u0007':
                text = re.sub(char, "", text)
        
        text = re.sub("\b", "", text)
        text = re.sub("\t", "", text)
        text = re.sub("\r", "", text)
        text = re.sub("\n", "", text)
        text = re.sub(" ", "", text)
        text = re.sub("　", "", text)
        text = re.sub("⁡", "", text)
        text = re.sub(r"\ {5,}", "", text)

        # remove citations
        text = re.sub(r"(\[[1-9][0-9]*\]|\[([1-9][0-9]*,?-?−? ?)+[1-9][0-9]*\])", "", text)

        # remove links
        text = re.sub(r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)", "", text)

        # choose specific text to replace/remove depending on the datasource
        match (source):
            case "ictp":
                if (re.search(r"^([1-9][0-9]*\.+)+[1-9][0-9]*", text)):
                    title = text
                    continue

                if (title != ""):
                    text = title + "\n" + text
                    title = ""
            case "caict":
                text = re.sub(r"[0-9]{8,}", "", text)
                text = re.sub(r"(SïOáS:WWþc¨Û¡R.+)", "", text)
            case "hkCertEN":
                if (text == "Reference:") or (text == "Reference Links:") or (text == "Articles that we like:") or (text == "Article written by HKCERT on Hong Kong Economic Times:"):
                    continue
                if ("Hong Kong Computer Emergency Response Team (HKCERT) Coordination Centre cooperates with the National Institute of Network and Information Security (NINIS) for detecting malicious and suspicious behaviors of Apps from the Google Play Store, in order to study the security risk of apps in the Google Play Store in Hong Kong area. NINIS provides us analyzed result, and we collate the detection result and publish security alerts to the public." in text):
                    continue
                if (re.search(r"(Favourite[\ ]+Security Reads)", text, re.I)):
                    continue
            case "hkCertTC":
                if (text == "參考") or (text == "參考資料") or (text == "參考連結：") or (text == "下面是本週的最愛。"):
                    continue
                if (re.search(r"(每週最愛保安閱讀)|(最愛保安閱讀雙週)|(HKCERT 編寫的)", text)):
                    continue
            case "zte":
                text = re.sub(r"(七七)", "", text)
                text = re.sub(r"(•)", "", text)
                text = re.sub(r"(\*)", "", text)
                text = re.sub(r"[0-9]*(专题ZTE TECHNOLOGY JOURNAL)", "", text)
            case "jeit":
                if ("尊敬的读者" in text): continue
                if (text == "HTML全文"): continue
                if ("Copyright" in text): continue
                if ("中国科学院电子学研究所" in text): continue
                if ("电话：" in text): continue
                if ("中图分类号" in text): continue
                if ("年生" in text): continue
                if ("微信图文分享好友和朋友圈" in text): continue
                if ("目录" in text): continue
            case "xidian":
                if ("西安电子科技大学学报" in text): continue
                if ("DOI" in text): continue
                if ("doi" in text): continue
                if ("本文引用" in text): continue
                if ("收稿日期" in text): continue
                if ("Received:" in text): continue
                if ("关键词" in text): continue
                if ("Keywords：" in text): continue
            case "sciEngineEN":
                if ("Editorial" in text): continue
                if ("© The Author(s)" in text): continue
                if ("This is an Open Access" in text): continue
                if (text.startswith("Citation")): continue
            case "SSI":
                if ("Support format" in text): continue
                if ("Advanced Search" in text): continue
                if ("View allresults" in text): continue
                if ("NetworkPositioningSearch" in text): continue
                if ("undefinedundefined" in text): continue
                if ("No related articles have been found" in text): continue
                if ("Accepted" in text): continue
                text = re.sub(r"\(Color online\) ", "", text)
                text = re.sub(r"\\\\", "", text)
            case "3gpp":
                if ("Error! No text of specified style in document." in text): continue
        
        if (len(text) <= cutoffLen):
            continue

        returnList.append(text)
        # print(len(returnList))
        # print(returnList)

    # Closing file
    f.close()

    return returnList

### .doc to .docx conversion specifically cannot utilize multiprocessing, as it depends on external software to be installed
def doc2docxConverter(sourceFolder : str, destFolder : str, docList : str, startIndex : int, endIndex : int):
    """Converts .doc files to .docx files, theoretically can be called by multiprocessing code

    Args:
        sourceFolder (str): File path of input folder (that contains .doc files)
        destFolder (str): File path of desired output folder (can be the same as input folder)
        docList (str): List of .doc files
        startIndex (int): Desired start index in docList
        endIndex (int): Desired end index in docList
        name (str): Name of process
    """    
    #print(docList)
    print(docList[startIndex:endIndex])

    ### theoretical conversion code for Windows & Mac with Microsoft Word installed
    for i in trange(startIndex, endIndex):
        print("\n" + str(i) + "/" + str(endIndex))
        convert(os.path.join(sourceFolder, docList[i]), os.path.join(destFolder, ""))
        print('success!')
    ###


    ### Conversion code that uses LibreOffice
    # for i in trange(startIndex, endIndex):
    #     print("\n" + name + ": " + str(i) + "/" + str(endIndex))
        
    #     file = (sourceFolder + '/' + docList[i])
    #     print("\n" + file)
    #     output = subprocess.check_output([
    #         "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    #         "--headless",
    #         "--convert-to",
    #         "docx",
    #         file,
    #         "--outdir",
    #         destFolder])
        # print('success!')
    ###

def doc2docx(sourceFolder : str, destFolder : str, NUM_SECTIONS : int):
    """Converts a .doc files in a folder to .docx files

    Args:
        sourceFolder (str): File path of input folder (containing .doc files)
        destFolder (str): File path of desired output folder (can be the same folder)
        # NUM_SECTIONS (int): Number of sections to divide the total set of files up into (i.e. the number of processes that will run)
    """    
    g = os.listdir(sourceFolder)
    docList = [f for f in g if f.endswith(('.doc'))]
    # processList = []

    # # section size calculation for multiprocessing
    # totalSize = len(docList)
    # remainder = totalSize % NUM_SECTIONS
    # sectionSize = (totalSize - remainder) // NUM_SECTIONS

    # # assign sections to processes
    # for sectionIndex in range(0, NUM_SECTIONS):
    #     startOffset = sectionSize * sectionIndex
    #     endOffset = sectionSize * (sectionIndex + 1)
    #     name = "P" + str(sectionIndex)
    #     print("startOffset: " + str(startOffset))
    #     print("endOffset: " + str(endOffset))
    #     if (sectionIndex != (NUM_SECTIONS - 1)):
    #         process = multiprocessing.Process(target=doc2docxConverter, args=(sourceFolder, destFolder, docList, startOffset, endOffset, name))
    #     else:
    #         process = multiprocessing.Process(target=doc2docxConverter, args=(sourceFolder, destFolder, docList, startOffset, endOffset + remainder, name))
    #     processList.append(process)

    # # start & join processes
    # for process in processList:
    #     process.start()

    # for process in processList:
    #     process.join()

    doc2docxConverter(sourceFolder, destFolder, docList, 0, len(docList))

def docx2list(docxFile : str) -> list[str]:
    """Converts .docx file into a list of strings

    Args:
        docxFile (str): input file path of .docx file

    Returns:
        list[str]: list of strings, extracted from text in .docx file
    """    
    docxStr = docx2txt.process(docxFile)
    docxStr = re.sub(r'^$\n', '', docxStr, flags=re.MULTILINE)
    #print(docxStr)

    li = list(docxStr.split("\n"))
    return li

def docx2JsonConverter(sourceFolder : str, destFolder : str, docxList : list[str], startIndex : int, endIndex : int, name : str):
    """Converter function, called by docx2Json

    Args:
        sourceFolder (str): File path of source folder (of docx files)
        destFolder (str): File path of destination folder (of docx files)
        docxList (list[str]): List of docx files
        startIndex (int): starting index
        endIndex (int): ending index
        name (str): process name
    """    
    fullText = []
    for i in trange(startIndex, endIndex):
        print("\n" + name + ": " + str(i) + "/" + str(endIndex))
        fullText.extend(docx2list(os.path.join(sourceFolder, docxList[i])))
        print('success!')
    list2json(fullText, os.path.join(destFolder, name) + ".json")

def docx2Json(sourceFolder : str, destFolder : str, NUM_SECTIONS : int):
    """Converts a folder of docx files to json files using multiprocessing

    Args:
        sourceFolder (str): File path to source folder
        destFolder (str): File path to destination folder
        NUM_SECTIONS (int): number of processes to separate into
    """    
    g = os.listdir(sourceFolder)
    docxList = [f for f in g if f.endswith(('.docx'))]
    processList = []
    # section size calculation for multiprocessing
    totalSize = len(docxList)
    remainder = totalSize % NUM_SECTIONS
    sectionSize = (totalSize - remainder) // NUM_SECTIONS

    # assign sections to processes
    for sectionIndex in range(0, NUM_SECTIONS):
        startOffset = sectionSize * sectionIndex
        endOffset = sectionSize * (sectionIndex + 1)
        name = "P" + str(sectionIndex)
        print("startOffset: " + str(startOffset))
        print("endOffset: " + str(endOffset))
        if (sectionIndex != (NUM_SECTIONS - 1)):
            process = multiprocessing.Process(target=docx2JsonConverter, args=(sourceFolder, destFolder, docxList, startOffset, endOffset, name))
        else:
            process = multiprocessing.Process(target=docx2JsonConverter, args=(sourceFolder, destFolder, docxList, startOffset, endOffset + remainder, name))
        processList.append(process)

    # start & join processes
    for process in processList:
        process.start()

    for process in processList:
        process.join()

def doc2json(sourceFolder : str, destFile : str, NUM_SECTIONS : int):
    """Full pipeline for converting .doc files to JSON files

    Args:
        sourceFolder (str): File path of input folder (containing .doc files)
        destFile (str): File path of desired output JSON file
        NUM_SECTIONS (int): Number of sections to divide the total set of files up into (i.e. the number of processes that will run)
    """    
    fullText = []
    #convert doc to docx within the same folder
    doc2docx(sourceFolder, sourceFolder, NUM_SECTIONS)

    # get all docx files and append them to list of text
    g = os.listdir(sourceFolder)
    file_path = [f for f in g if f.endswith(('.docx'))]
    #print(file_path)
    for i in file_path:
        file = (sourceFolder + '/' + i)
        fullText.extend(docx2list(file))
    
    list2json(fullText, destFile)