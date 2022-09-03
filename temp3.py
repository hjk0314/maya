import pandas as pd
import pyodbc
import urllib
from sqlalchemy import create_engine


# using urlib
# using sqlalchemy
# using pandas
def usingSqlalchemy():
    conn_str = (
        r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=../folder/file.accdb;'
    )
    conn_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}"
    acc_engine = create_engine(conn_url)
    csv_path = "../folder/file.csv"
    csv_data = pd.read_csv(csv_path)
    csv_data.to_sql('table', acc_engine, if_exists='append', index=False)


# using pyodbc only
def usingPyodbc():
    conn_str = (
        r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=../folder/file.accdb;'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    # insert
    sql = r"Insert into tabel (uName, wDate) Values ('jkhng', '2022-09-03')"
    cursor.execute(sql)
    cursor.commit()
    # select all
    sql = r"select * from table"
    cursor.excute(sql)
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()


# using pandas
# using pyodbc
def usingPandas():
    conn_str = (
        r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=../folder/file.accdb;'
    )
    conn = pyodbc.connect(conn_str)
    sql = r"Select * From table"
    df = pd.read_spl(sql, conn)
    wDate  = [str(i) for i in df['wDate'] if str(i).startswith('2022-05')]
    print(wDate)
    print(df.head(3))
    conn.close()

