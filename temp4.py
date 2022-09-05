import os
import codecs
import pandas as pd
import pyodbc
import urllib
from sqlalchemy import create_engine


def saveAs():
    csv_folder = "W:/SP팀/크루플랜/2022"
    csv_newFolder = "C:/Users/jkhong/Desktop/크루플랜_테스트"
    csv_files = os.listdir(csv_folder)
    for i in csv_files:
        csv_old = csv_folder + '/' + i
        if os.path.isfile(csv_old):
            csv_new = csv_newFolder + '/' + i
            with open(csv_old, 'r') as txtOld:
                lines = txtOld.readlines()
            if lines:
                with codecs.open(csv_new, 'w', 'utf-8-sig') as txtNew:
                    txtNew.writelines(lines)
            else:
                print(f"No data : {i}")
        else:
            pass


# using urlib
# using sqlalchemy
# using pandas
def usingSqlalchemy():
    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=C:\Users\jkhong\Desktop\크루플랜_테스트\crewPlan.accdb;"
    )
    conn_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}"
    acc_engine = create_engine(conn_url)
    csv_folder = "C:/Users/jkhong/Desktop/크루플랜_테스트/csv_copied"
    csv_files = os.listdir(csv_folder)
    for i in csv_files:
        csv_file = csv_folder + '/' + i
        if os.path.isfile(csv_file):
            try:
                df = pd.read_csv(csv_file)
                df.to_sql('2022', acc_engine, if_exists='append', index=True)
            except:
                print(f'Error : {i}')
                continue
        else:
            pass

