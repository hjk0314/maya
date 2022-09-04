import os
import codecs
import pandas as pd
import pyodbc
import urllib
from sqlalchemy import create_engine


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


# using urlib
# using sqlalchemy
# using pandas
def usingSqlalchemy():
    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=C:\Users\hjk03\Desktop\crewPlan\crewPlanDB.accdb;"
    )
    conn_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}"
    acc_engine = create_engine(conn_url)
    csv_folder = "C:/Users/hjk03/Desktop/crewPlan/csv/new"
    csv_files = os.listdir(csv_folder)
    for i in csv_files:
        csv_file = csv_folder + '/' + i
        if os.path.isfile(csv_file):
            try:
                df = pd.read_csv(csv_file)
                print(df.head(1))
                df.to_sql('2022', acc_engine, if_exists='append', index=True)
            except:
                print('this')
                continue
        else:
            pass


usingSqlalchemy()