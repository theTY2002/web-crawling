import random
from functions import *

# hkCertENList = jsonReadNClean("hkCertENCleaned.json", 300, "hkCertEN")
# testList = []

# for i in range(0, 20):
#     currText = hkCertENList.pop(random.randrange(len(hkCertENList)))
#     testList.append(currText)

# list2json(testList, "questions.json")

sciEngineENList = jsonReadNClean("sciEngineENCleaned.json", 100, "sciEngineEN")
testList = []

for i in range(0, 20):
    currText = sciEngineENList.pop(random.randrange(len(sciEngineENList)))
    testList.append(currText)

list2json(testList, "questions.json")