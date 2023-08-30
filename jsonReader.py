### Main function for cleaning junk data from json files

from functions import *

# ictpList = jsonReadNClean("ictp.json", 10, "ictp")

# list2json(ictpList, "ictpCleaned.json")



# caictList = []
# fileCount = 0
# for file in os.listdir("downloads/caictJson"):   # get the list of files
#     if file.startswith('.'):
#             continue
#     #print(file)
#     fileCount += 1
#     caictList.extend(jsonReadNClean("downloads/caictJson/" + str(file), 10, "caict"))

# print(fileCount)
# list2json(caictList, "caictCleaned.json")


# hkCertENList = jsonReadNClean("hkCertENCleaned.json", 300, "hkCertEN")

# list2json(hkCertENList, "hkCertENTestGenerator.json")


# hkCertTCList = jsonReadNClean("hkCertTC.json", 10, "hkCertTC")

# list2json(hkCertTCList, "hkCertTCCleaned.json")

# zteList = []
# fileCount = 0
# for file in os.listdir("downloads/zteJson"):   # get the list of files
#     if file.startswith('.'):
#             continue
#     #print(file)
#     fileCount += 1
#     zteList.extend(jsonReadNClean("downloads/zteJson/" + str(file), 10, "zte"))

# print(fileCount)
# list2json(zteList, "zteCleaned.json")

# dlxxtxList = jsonReadNClean("dlxxtx.json", 10, "dlxxtx")

# list2json(dlxxtxList, "dlxxtxCleaned.json")


# for i in range(2018, 2024):
#     jeitList = jsonReadNClean("jeit/jeit" + str(i) + ".json", 10, "jeit")

#     list2json(jeitList, "jeit/jeit" + str(i) + "Cleaned.json")

# buptList = jsonReadNClean("bupt.json", 10, "bupt")

# list2json(buptList, "buptCleaned.json")

# xidianList = jsonReadNClean("xidian.json", 10, "xidian")

# list2json(xidianList, "xidianCleaned.json")


sciEngineENList = jsonReadNClean("sciEngineEN.json", 100, "sciEngineEN")

list2json(sciEngineENList, "sciEngineENCleaned.json")

# for i in range(2014, 2024):
#     josList = jsonReadNClean("jos" + str(i) + ".json", 10, "jos")

#     list2json(josList, "jos/jos" + str(i) + "Cleaned.json")

# SSIList = []
# for i in range(0, 13):
#     SSIList.extend(jsonReadNClean("sciEngineCNmultiP" + str(i) + ".json", 10, "SSI"))

# list2json(SSIList, "SSI/SSICleaned.json")
