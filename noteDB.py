import itertools
import urllib
import pyodbc
import pandas as pd
from sqlalchemy import create_engine


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
    csv_path = r"C:\Users\hjk03\Desktop\crewPlan\csv\ANI_Team_NAME_data.csv"
    df = pd.read_csv(csv_path)
    df.to_sql('2022', acc_engine, if_exists='append', index=False)


# using pyodbc only
def usingPyodbc():
    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=C:\Users\hjk03\Desktop\crewPlan\crewPlanDB.accdb;"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    # insert
    sql = (
        r"INSERT INTO 2022 ([TEAM], [NAME], [DATE], [PROJ], [wTIME], [aTIME], [TYPE]) VALUES "
        r"('myTeam', 'myName', '2022-09-03', 'Voltron', 5.0, 5.0, 'normal')"
    )
    cursor.execute(sql)
    cursor.commit()
    # select
    sql = r"SELECT * FROM 2022"
    cursor.execute(sql)
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()


# using pandas
# using pyodbc
def usingPandas():
    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=C:\Users\hjk03\Desktop\crewPlan\crewPlanDB.accdb;"
    )
    conn = pyodbc.connect(conn_str)
    sql = r"SELECT * FROM 2022"
    df = pd.read_sql(sql, conn)
    wDate  = [str(i) for i in df['DATE'] if str(i).startswith('2022-05')]
    print(wDate)
    conn.close()


# 79 char line ================================================================
# 72 docstring or comments line ========================================




def num2Col(number: int) -> str:
    alpha = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    count = 0
    column = ''
    # count(1) -> 'A', 'B'
    # count(2) -> 'AA', 'AB'
    # count(3) -> 'AAA', 'AAB'
    for j in itertools.count(1):
        if count > number:
            break
        for k in itertools.product(alpha, repeat=j):
            count += 1
            if count > number:
                # yield ''.join(k)
                column = ''.join(k)
                break
    return column


def col2Num(column: str) -> int:
    alpha = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    count = 0
    isSame = False
    # count(1) -> 'A', 'B'
    # count(2) -> 'AA', 'AB'
    # count(3) -> 'AAA', 'AAB'
    for j in itertools.count(1):
        if isSame:
            break
        for k in itertools.product(alpha, repeat=j):
            if column == ''.join(k):
                isSame = True
                # yield count
                break
            count += 1
    return count

