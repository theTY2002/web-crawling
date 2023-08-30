# input: pdf files
# output: json files

# importing required modules
from functions import *

# for i in range(0, 310):
#     if (i == 191) or (i == 144):
#         continue
#     pdf2Json(2, 1, "downloads/caict/caict" + str(i) + ".pdf", "downloads/caictJson/caict" + str(i) + ".json", [r"（\s*[0-9]{4}\s*年）\s*[0-9]+", r"白皮书\s+"], False, "caict")

# pdf2Json(0, "/Users/trevor/Downloads/2.pdf", "zte.json", ["基于数字孪生网络的 6G无线网络自治 刘光毅  等 热点专题中兴通讯技术2023  年 6 月    第 29 卷第  3 期   Jun . 2023    Vol . 29  No. 3"])

# pdf2Json(4, 2, "downloads/zte0.pdf", "zte.json", [r"No. [0-9]"], True)

import zipfile, os

working_directory = '/Users/trevor/VSCode/downloads/zte/onlyPDF'
os.chdir(working_directory)

count = 0
for file in tqdm(os.listdir(working_directory)):   # get the list of files
    print(count)
    if (count == 51):
        count += 1
        continue
    pdf2Json(4, 2, file, "/Users/trevor/VSCode/downloads/zteJson/zte" + str(count) + ".json", [r"No. [0-9]"], True, "")
    count += 1