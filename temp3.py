import pandas as pd
import pyodbc
import urllib
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
    csv_path = r"C:\Users\hjk03\Desktop\crewPlan\csv\ANI_Team_황병식_data.csv"
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
        r"INSERT INTO 2022 ([부서], [이름], [날짜], [프로젝트], [투입시간], [총 근무시간], [근무형태]) VALUES "
        r"('도적단', '홍길동', '2022-09-03', '곳간 털기', 5.0, 5.0, '도둑질')"
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
    wDate  = [str(i) for i in df['날짜'] if str(i).startswith('2022-05')]
    print(wDate)
    conn.close()

