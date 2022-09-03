import os
import codecs


def saveAs():
    csv_folder = "C:/Users/hjk03/Desktop/crewPlan/csv"
    csv_newFolder = "C:/Users/hjk03/Desktop/crewPlan/csv/new"
    csv_files = os.listdir(csv_folder)
    for i in csv_files:
        csv_old = csv_folder + '/' + i
        if os.path.isfile(csv_old):
            csv_new = csv_newFolder + '/' + i
            with open(csv_old, 'r') as txtOld:
                lines = txtOld.readlines()
            with codecs.open(csv_new, 'w', 'utf-8') as txtNew:
                txtNew.writelines(lines)
        else:
            pass

