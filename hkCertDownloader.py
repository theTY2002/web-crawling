from functions import *

BASE_URL = "https://www.hkcert.org"
NUM_PAGES = 8
articleLinks = []

def getLinksFromSoup(soup : BeautifulSoup) -> list[str]:
    """Gets article links from BeautifulSoup object

    Args:
        soup (BeautifulSoup): BeautifulSoup object

    Returns:
        list[str]: list of article links
    """    
    articleLinks = []
    # finding links to HTML articles
    for a in soup.find_all("a", class_="listingcard__item"):
        articleLink = BASE_URL + a['href']
        articleLinks.append(articleLink)
        #print(articleLink)

    return articleLinks

### EN version download

page = 0
for i in range(1, NUM_PAGES + 1):
    print("page: " + str(page) + "/" + str(NUM_PAGES))
    page += 1
    contentsSoup = URLtoSoup("https://www.hkcert.org/blog?item_per_page=100&page=" + str(i))
    articleLinks.extend(getLinksFromSoup(contentsSoup))

print(articleLinks)

textList = []
count = 0
for articleLink in articleLinks:
    print("article: " + str(count) + "/" + str(len(articleLinks)))
    count += 1
    articleSoup = URLtoSoup(articleLink)
    for p in articleSoup.find_all('p', attrs={"class": None, "style": None}):
        text = p.get_text().strip()
        if (text != "") and ("https://" not in text) and ("http://" not in text) and (("We use cookies" not in text)):
            textList.append(text)
# print(textList)

list2json(textList, "hkCertEN.json")

### TC version download

articleLinks = []
page = 0
for i in range(1, NUM_PAGES + 1):
    print("page: " + str(page) + "/" + str(NUM_PAGES))
    page += 1
    contentsSoup = URLtoSoup("https://www.hkcert.org/tc/blog?item_per_page=100&page=" + str(i))
    articleLinks.extend(getLinksFromSoup(contentsSoup))

print(articleLinks)

textList = []
count = 0
for articleLink in articleLinks:
    print("article: " + str(count) + "/" + str(len(articleLinks)))
    count += 1
    articleSoup = URLtoSoup(articleLink)
    for p in articleSoup.find_all('p', attrs={"class": None, "style": None}):
        text = p.get_text().strip()
        if (text != "") and ("https://" not in text) and ("http://" not in text) and (("我們使用cookie" not in text)):
            textList.append(text)
# print(textList)

list2json(textList, "hkCertTC.json")