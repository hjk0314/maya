import os
import itertools
import codecs
import urllib
import maya.OpenMaya as om
import pymel.core as pm
import pandas as pd
import openpyxl
from sqlalchemy import create_engine


# 79 char line ================================================================
# 72 docstring or comments line ========================================


class CrewPlan():
    def __init__(self):
        self.DATE = '2022-08'
        self.CSV_PATH = 'W:/SP팀/크루플랜/2022/ANI_Team_홍진기_data.csv'
        self.ORG_PATH = 'W:/SP팀/크루플랜/크루플랜(2022)_v01.xlsx'
        self.ALPHA = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.PROJ = {
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
            "범죄3": "P_범죄3", 
        }
        self.main()


    def main(self):
        PATH = self.copyCSV()
        data = self.readCSV(PATH)
        self.makeValues(data)


    # Read the csv file.
    def readCSV(self, PATH):
        df = pd.read_csv(PATH)
        data = df['날짜'].str.contains(self.DATE)
        return df[data] # class: 'pandas.core.frame.DataFrame'


    # Make the sheet name and value.
    def makeValues(self, df):
        pass


    # Number converted to column character.
    def num2Col(self, number: int) -> str:
        count = 0
        column = ''
        # count(1): 'A', 'B'
        # count(2): 'AA', 'AB'
        # count(3): 'AAA', 'AAB'
        for j in itertools.count(1):
            if count > number:
                break
            for k in itertools.product(self.ALPHA, repeat=j):
                count += 1
                if count > number:
                    column = ''.join(k)
                    break
        return column


    # Column character converted to number.
    def col2Num(self, column: str) -> int:
        count = 0
        isSame = False
        # count(1): 'A', 'B'
        # count(2): 'AA', 'AB'
        # count(3): 'AAA', 'AAB'
        for j in itertools.count(1):
            if isSame:
                break
            for k in itertools.product(self.ALPHA, repeat=j):
                if column == ''.join(k):
                    isSame = True
                    break
                count += 1
        return count


    # Check the conditions.
    def conditions(self):
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
            om.MGlobal.displayInfo('Successfully done.')


    def writeExcel(self):
        pass


    # CSV file is copied and returned.
    def copyCSV(self) -> str:
        (name, ext) = os.path.splitext(self.CSV_PATH)
        NEW_PATH = name + '_sig' + ext
        with open(self.CSV_PATH, 'r') as file:
            lines = file.readlines()
        with codecs.open(NEW_PATH, 'w', 'utf-8-sig') as newFile:
            newFile.writelines(lines)
        return NEW_PATH


