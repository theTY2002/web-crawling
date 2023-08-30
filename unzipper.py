### Unzips all .zip files within a folder

import zipfile, os
from tqdm import *

def unzipFiles(sourceFolder : str, destFolder : str, startIndex = 0):
    """Unzips all files in sourceFolder, and outputs results to destFolder

    Args:
        sourceFolder (str): File path of source (input) folder
        destFolder (str): File path of destination (output) folder; can be the same as input
        startIndex (int): starting index of folder; optional
    """    
    os.chdir(sourceFolder)
    fileList = os.listdir(sourceFolder)
    for i in trange(startIndex, len(fileList)):   # get the list of files
        file = fileList[i]
        if zipfile.is_zipfile(file): # if it is a zipfile, extract it
            with zipfile.ZipFile(file) as item: # treat the file as a zip
                try:
                    item.extractall(destFolder)  # extract it in the working directory
                except Exception as e:
                    print(e)

#unzipFiles("/Users/trevor/VSCode/3gppZip", "/Users/trevor/VSCode/docFiles")