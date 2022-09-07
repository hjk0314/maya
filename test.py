import openpyxl
import os
import itertools
import datetime
import csv
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
import urllib


class crew():
    def __init__(self):
        self.csvFolder = "Y:/personal/hjk2"
        self.csvFile = '' # '../folder/*.csv'
        self.orgFile = '' # '../folder/*.xlsx'
        self.col = 'HP' # 'FE', 'GJ', 'HP'
        self.row = '70' # '70'
        self.alpha = [chr(i) for i in range(ord('A'), ord('Z') + 1)] # ['A', 'B', 'C', ... 'Z']
        self.colList = []
        yyyymmdd = datetime.date.today() # '2022-08-31'
        temp = yyyymmdd.split("-") # ['2022', '08', '31']
        yyyy = temp[0] # '2022'
        mm = temp[1] # '08'
        dd = temp[2] # '31'
        self.shDict = {
            "기타": "기타", 
            "핸썸가이즈": "A_핸썸가이즈", 
            "크리스마스선물": "B_크리스마스선물", 
            "해피뉴이어": "C_해피뉴이어", 
            "한산": "D_한산", 
            "범죄2": "E_범죄2", 
            "재벌집": "G_재벌집", 
            "모럴센스": "F_모럴센스", 
            "패뷸러스": "I_패뷸러스", 
            "오픈더도어": "J_오픈더도어", 
            "말할수없는비밀": "H_말할수없는비밀", 
            "도적": "K_도적", 
            "서울의봄": "L_서울의봄", 
            "피랍": "M_피랍", 
            "마스크걸": "N_마스크걸", 
            "하얼빈": "O_하얼빈", 
            "범죄3": "P_범죄3"
        }
        csvData = [] # [['yymmdd', 'name', ... 'typ'], ['yymmdd', 'name', ... 'typ'], ...]
        val = 0.0
        shName = '' # '재벌집', '도적', ...


        self.getCsvData
        self.conditions
        self.writeExcel
        self.col2Num
        self.num2Col
        self.makeVal
        # self.makeCsv
        self.main


    def conditions(self):
        pass


    def writeExcel(self):
        pass


    def getCsvData(self, csvPath):
        year = self.yearField.getValue()
        month = self.monthField.getValue()
        month = int(month)
        month = '%02d' % month
        date = f"{year}-{month}"
        with open(csvPath, 'r') as file:
            data = file.readlines()
        dataList = []
        for i in data:
            i = i.replace("\n", "")
            line = i.split(",")
            if line[2].startswith(date):
                dataList.append(line[2:7])
            else:
                continue
        return dataList


    def num2Col(self, number): # number = int
        count = 0
        column = ''
        # count(1) -> 'A', 'B'
        # count(2) -> 'AA', 'AB'
        # count(3) -> 'AAA', 'AAB'
        for j in itertools.count(1):
            if count > number:
                break
            for k in itertools.product(self.alpha, repeat=j):
                count += 1
                if count > number:
                    # yield ''.join(k)
                    column = ''.join(k)
                    break
        return column


    def col2Num(self, column): # column = str
        count = 0
        isSame = False
        # count(1) -> 'A', 'B'
        # count(2) -> 'AA', 'AB'
        # count(3) -> 'AAA', 'AAB'
        for j in itertools.count(1):
            if isSame:
                break
            for k in itertools.product(self.alpha, repeat=j):
                if column == ''.join(k):
                    isSame = True
                    # yield count
                    break
                count += 1
        return count


    def makeVal(self, csvData):
        pass
        # r_sheet = sheet
        # value = wTime
        # if typ == '휴가':
        #     r_sheet = '기타'
        #     value = '휴'
        # elif typ == '반차':
        #     r_sheet = sheet
        #     value = '반' if sheet == '기타' and wTime == '0.0' else (float(wTime) / 8)
        # elif typ == '정상근무':
        #     r_sheet = sheet
        #     value = float(wTime) / float(sum)
        # elif typ == '기타':
        #     r_sheet = sheet
        #     value = float(wTime) / float(sum)
        # else:
        #     r_sheet = ''
        #     value = 0
        # return r_sheet, value


    # Main Function.
    def main(self):
        column = self.columnField.getText()
        userRow = self.userRowField.getText()
        csvPath = self.csvField.getText()
        orgPath = self.OriginFile.getText()
        if not column:
            pass
        elif not column.isalpha():
            pass
        elif not userRow:
            pass
        elif not userRow.isdigit():
            pass
        elif not csvPath:
            pass
        elif not orgPath:
            pass
        else:
            column = column.upper() # GJ, HP 
            userRow = int(userRow)
            month = self.monthField.getValue() # '8'
            month = int(month) # '8' -> 8
            day = self.getDayCount(month) # 8 -> 31
            data = self.getCsvInfo(csvPath) # [['2022-08-01', 'Etc', '0.0', '8.0', 'Normal'], ['2022-08-01', 'DOJ', '8.0', '8.0', 'Normal'], ...
            num = self.columnToNumber(column) # HP -> 223
            columnList = [self.numberToColumn(i) for i in range(num, num + day)]
            loadExcel = openpyxl.load_workbook(orgPath)
            for i in data:
                date = i[0]
                date = date.split("-")[-1]
                date = int(date)
                idx = date - 1
                colRow = columnList[idx] + str(userRow)
                sheetValue, cellValue = self.getInputData(i[1], i[2], i[3], i[4])
                if sheetValue == '기타' and cellValue == 0.0:
                    pass
                else:
                    try:
                        float(cellValue)
                    except:
                        pass
                    sName = loadExcel[self.sheetDict[sheetValue]]
                    sName[colRow] = cellValue
            loadExcel.save(orgPath)


def test():
    csvFolder = "Y:/personal/hjk2"
    csvFile = csvFolder + "/jkhong.csv"
    data = pd.read_csv(csvFile, sep=',')
    # print(data[data['wType']=='휴가'])
    # print(data[data.wDate == '2022-09-08'])
    # data.uName = data.uName.replace('홍진기', '황병식')
    # data.to_csv(csvFile, sep=',', index=False)
    # with open(csvFile, 'a+', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['Ani', '홍진기', '2022-09-01', '기타', 8.0, '정상근무'])



        # for row in reader:
        #     yyyymmdd = datetime.date.today() # '2022-08-31'
        #     temp = yyyymmdd.split("-") # ['2022', '08', '31']
        #     yyyy = temp[0] # '2022'
        #     mm = temp[1] # '08'
        #     dd = temp[2] # '31'
        #     idx = f"{yyyy}-{mm}"
# dir = "Y:/personal/hjk2"
# csvFolder = os.listdir(dir)
# csvFile = [dir + '/' + i for i in csvFolder if i.endswith('.py')]
# print(csvFile)

test()


# Convert number to column character in excel.
def numberToColumn(number):
    if not number.isdigit():
        print('Number only.')
    else:
        # ['A', 'B', 'C', ... 'Z']
        alpha = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        count = 0
        for j in itertools.count(1): # count(1) -> 'A', 'B' / count(2) -> 'AA', 'AB' / count(3) -> 'AAA', 'AAB'
            if count > number:
                break
            for k in itertools.product(alpha, repeat=j):
                count += 1
                if count > number:
                    yield ''.join(k)
                    break


# Convert column letters to numbers in Excel.
def columnToNumber(column):
    if not column.isalpha():
        print('Alphabet only.')
    else:
        alpha = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        count = 0
        isSame = False
        for j in itertools.count(1): # count(1) -> 'A', 'B' / count(2) -> 'AA', 'AB' / count(3) -> 'AAA', 'AAB'
            if isSame:
                break
            for k in itertools.product(alpha, repeat=j):
                if column == ''.join(k):
                    isSame = True
                    yield count
                    break
                count += 1


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
        r"INSERT INTO 2022 ([TEAM], [NAME], [DATE], [PROJECT], [wTIME], [aTIME], [TYPE]) VALUES "
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

