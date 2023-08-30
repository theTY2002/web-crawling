from functions import *

if __name__ == '__main__':
    # doc2json("/Users/trevor/VSCode/docFiles", "3gppDocx.json", 1)
    doc2docx("/Users/trevor/VSCode/docFiles", "/Users/trevor/VSCode/docFiles", 1)

# cleanList = jsonReadNClean("3gpp.json", 10, "3gpp")
# list2json(cleanList, "3gppCleaned.json")

###Solution 1: tank the 60 hour conversion time
###Solution 2: get Microsoft Word
###Solution 3: local conversion on windows