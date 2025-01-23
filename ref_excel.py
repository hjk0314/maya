import itertools
import urllib
import pyodbc
import openpyxl
import pandas as pd
from sqlalchemy import create_engine


def csvToAccess():
    """ Send csv file to "MS Access DB" using pandas"""
    CSV_PATH = '../folder/file.csv'
    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=../folder/file.accdb;"
    )
    conn_str = urllib.parse.quote_plus(conn_str)
    conn_url = f'access+pyodbc:///?odbc_connect={conn_str}'
    acc_engine = create_engine(conn_url)
    df = pd.read_csv(CSV_PATH, encoding='ANSI')
    # df.to_csv(CSV_PATH, index=False, encoding='utf-8')
    df.to_sql('TABLE', acc_engine, if_exists='append', index=False)


def sqlToAccess():
    """ Insert SQL to MS Access using pyodbc """
    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=../folder/file.accdb;"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    sql = (
        r'INSERT INTO "table" (["team"], ["name"], ["date"]) VALUES '
        r'("myTeam", "myName", "2022-09-08")'
    )
    cursor.execute(sql)
    cursor.commit()
    # sql = r'SELECT * FROM table'
    # cursor.execute(sql)
    # for row in cursor.fetchall():
    #     print(row)
    cursor.close()
    conn.close()


def readDB():
    """ Read Data from MS Access DB using pyodbc, pandas """
    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=../folder/file.accdb;"
    )
    conn = pyodbc.connect(conn_str)
    sql = r"SELECT * FROM table"
    df = pd.read_sql(sql, conn)
    data = df['DATE'].str.contains('2022-08')
    # data = [str(i) for i in df['DATE'] if str(i).startswith('2022-05')]
    conn.close()


def numberToAlphabet(number: int) -> str:
    """ Change numbers to alphabets for MS Excel.
    >>> numberToAlphabet(0)
    >>> A
    >>> numberToAlphabet(35)
    >>> AJ
    >>> numberToAlphabet(1000)
    >>> ALM
     """
    alphabets = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    count = 0
    column = ''
    # count(1) -> 'A', 'B'
    # count(2) -> 'AA', 'AB'
    # count(3) -> 'AAA', 'AAB'
    for j in itertools.count(1):
        if count > number:
            break
        for k in itertools.product(alphabets, repeat=j):
            count += 1
            if count > number:
                # yield ''.join(k)
                column = ''.join(k)
                break
    return column


def alphabetToNumber(column: str) -> int:
    """ Change Alphabet to number for MS Excel. 
    >>> alphabetToNumber("A")
    >>> 0
    >>> alphabetToNumber("AC")
    >>> 28
    >>> alphabetToNumber("ATM")
    >>> 1208
    >>> alphabetToNumber("atm")
    >>> None
     """
    alphabets = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    count = 0
    isSame = False
    # count(1) -> 'A', 'B'
    # count(2) -> 'AA', 'AB'
    # count(3) -> 'AAA', 'AAB'
    for j in itertools.count(1):
        if isSame:
            break
        for k in itertools.product(alphabets, repeat=j):
            if column == ''.join(k):
                isSame = True
                # yield count
                break
            count += 1
    return count


def writeToExcel():
    """ Write somethings to MS Excel using openpyxl. """
    EXCEL_PATH = '../folder/file.xlsx'
    loadExcel = openpyxl.load_workbook(EXCEL_PATH)
    SHEET = loadExcel['Sheet1']
    SHEET['A1'] = 2.0
    loadExcel.save(EXCEL_PATH)

