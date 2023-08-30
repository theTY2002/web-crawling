#input: ictp URLs
#output: json files

from functions import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEBUG = True
BASE_URL = "http://ictp.caict.ac.cn/"
articleLinks = []
START_PAGE = 1
END_PAGE = 43
#wait time in seconds
DOWNLOAD_WAIT_TIME = 10


def getLinksFromSoup(soup):
    articleLinks = []
    # finding links to HTML articles
    #print(soup.find_all("a", target="_blank"))
    for a in soup.find_all("a", target="_blank"):
        articleLinks.append(a["href"])
        #print(a["href"])
    return articleLinks

# def getLinksFromURL(url):

#     # Making a GET request
#     r = requests.get(url)

#     # Parsing the HTML
#     soup = BeautifulSoup(r.content, 'html.parser')

#     for a in soup.find_all('a', href=True):
#         link = a['href'][1:]
#         if(link.endswith('.pdf')):
#             pdfList.append(pwd(url) + link)


humanReadable = []
for num in range(START_PAGE, END_PAGE + 1):
    if (DEBUG): print("page: " + str(num) + "/" + str(END_PAGE))
    pageURL = "http://ictp.caict.ac.cn/CN/volumn/volumn_"+ str(num) + ".shtml"
    if (DEBUG): print("pageURL: " + pageURL)
    contentsSoup = URLtoSoup(pageURL)
    articleLinks.extend(getLinksFromSoup(contentsSoup))
    if (DEBUG): print("articleLinks length: " + str(len(articleLinks)))

#print(articleLinks)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
# doesn't work
#options.add_argument(f"--download.default_directory={'/Users/trevor/VSCode/downloads'}")

service = Service()
driver = webdriver.Chrome(service=service, options=options)

count = 0
#for articleLink in articleLinks:
for i in range(20, len(articleLinks)):
    print(str(i) + "/" + str(len(articleLinks)))
    driver.get(articleLinks[i])
    print(articleLinks[i])
    #time.sleep(DOWNLOAD_WAIT_TIME)
    link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[href='#1']")))
    print(link)
    link.click()
    time.sleep(DOWNLOAD_WAIT_TIME)
    count += 1

# list2json(humanReadable, "ictp.json")