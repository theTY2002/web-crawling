### Outdated

import docx2txt
import re
from functions import *

def docx2json(docxFile : str, jsonFile : str):
    # replace following line with location of your .docx file
    docxStr = docx2txt.process(docxFile)
    docxStr = re.sub(r'^$\n', '', docxStr, flags=re.MULTILINE)
    #print(docxStr)


    li = list(docxStr.split("\n"))
    print(li)

    list2json(li, jsonFile)

    # cleanList = jsonReadNClean("test.json", 10, "3gpp")
    # list2json(cleanList, "testCleaned.json")

docx2json("/Users/trevor/VSCode/docxFiles/21101_CR0074_(Rel-10).docx", "test.json")