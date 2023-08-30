#source and dest can be the same, since there are doc files mixed with docx files

import os
import subprocess

source = "/Users/trevor/VSCode/docFiles"
dest = "/Users/trevor/VSCode/docxFiles"# 提前建好
app_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"# LibreOffice的安装路径

def doc2docx(source, dest, app_path):
    g = os.listdir(source)
    file_path = [f for f in g if f.endswith(('.doc'))]
    print(file_path)
    for i in file_path:
        file = (source + '/' + i)
        print(file)
        output = subprocess.check_output([
            app_path,
            "--headless",
            "--convert-to",
            "docx",
            file,
            "--outdir",
            dest])
        print('success!')


        #convert this to multiprocessing
        #what data needs to be kept; moving doc and docx files around

doc2docx(source, dest, app_path)