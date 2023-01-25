import pymel.core as pm
import maya.mel as mel
import re
import os


folder = "U:/DOJ/Rnd/Horse/Output/ABC/horseGroomV0006_sim_v0102"
searchList = ['hair', 'add', ]
extension = '.abc'
fileList = os.listdir(folder)
for i in fileList:
    name, ext = os.path.splitext(i)
    for j in searchList:
        if ext != extension:
            continue
        elif re.match(f'.*{j}.*', i):
            print(f"{folder}/{i}")
            pm.importFile(f"{folder}/{i}")
        else:
            print(f"There are no files matching the {j}")

    #     tmp.group(1)

    # print(checkList)
    # for k in checkList:
    #     if ext == extension:
    #     else:
    #         continue


# for i in sel:
#     tmp = re.match(f'(.*){search}(.*)', i)

# print(tmp)

