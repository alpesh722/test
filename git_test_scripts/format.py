# Script works only if 'black' is installed on system.
# This script is used to add header information in all .py scripts in a dir.
# Also all .py files will be formatted using black.


import os
import sys
import time
import subprocess

line1 = "# " * 40
line2 = "#!/usr/bin/python3"
line3 = "# Copyright (c) 2023, System Level Solutions (India) Pvt. Ltd."
line4 = "# "
line5 = "# Purpose   : Chassis Manager Feature Test"
line6 = "# Package   : python_scripts"
line8 = "# Project   : DELL CM "

# get current working directory
input_path = input("Provide path:\n")
os.chdir(input_path)
print("Foormatting files at : {}".format(os.getcwd()))
x = input("Go ahead [Y/N] ?")
if x.lower() == "y":
    pass
else:
    sys.exit()
folder_path = os.getcwd().replace("\\", "//")
# create empty set
list_path = set()
# get path of only .py files from current directory tree
for path, directories, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            list_path.add(os.path.join(path).replace("\\", "//"))

# print(list_path)
for path in list_path:
    # change directory path to obtain file data
    os.chdir(folder_path + path[1:])
    print(os.getcwd())    
    # get file list in current working directory
    list_file = os.listdir()
    # print(list_file)
    for file in list_file:
        # find python files and omit current file
        if file.endswith(".py") and file != os.path.basename(__file__):  # sys.argv[0]:
            print(file)
            line7 = "# File name : {}".format(file)
            txt1 = "\n".join(
                [line1, line2, line3, line4, line5, line6, line7, line8, line1]
            )
            with open(file, "r+") as f:
                old = f.read()  # read everything in the file
                check = old.splitlines()[6]                
                if line7 == check:
                    continue                
                f.seek(0)  # goto beginning location in the file
                f.write(txt1 + "\n" + old)  # write required line before
            
            time.sleep(1)
            # format using black in all files
            p = subprocess.Popen("black {}".format(file),
                                 stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            output = ""
            time.sleep(2)
            for line in p.stdout:
                output += line.decode("utf-8")

            print(output)
            if "All done!" not in output:
                print("ERROR: Can't perform formatting: {}".format(\
                    folder_path + path[1:]+ "//"+ file))
                pass
            # elif "No Python files are present to be formatted. Nothing to do" in output:
            #     pass

print(line4*5," Task Completed ", line4*5)