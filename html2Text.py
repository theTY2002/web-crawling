# Converts HTML files within a folder to text

from bs4 import BeautifulSoup
import os

directory = "/Users/trevor/Downloads/01_NE40E知识库/Unzipped"

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    
    ext = os.path.splitext(filename)[-1].lower()

    # Now we can simply use == to check for equality, no need for wildcards.
    if ext == ".htm":
        HTMLFileToBeOpened = open(directory + "/" + filename, "r")


    # Reading the file and storing in a variable
    contents = HTMLFileToBeOpened.read()

    # Creating a BeautifulSoup object and
    # specifying the parser
    beautifulSoupText = BeautifulSoup(contents, 'lxml')


    textList = beautifulSoupText.find_all("p")
    for text in textList:
        soup = text
        rawText = soup.get_text().strip()
        print(rawText)
