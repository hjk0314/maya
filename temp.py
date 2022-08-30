import pymel.core as pm
import openpyxl
import os
import itertools


class crewPlan():
    def __init__(self):
        self.userName = ''
        self.myCrewPlanPath = pm.internalVar(uad=True) + 'myCrewPlanPath.txt'
        self.myCrewPlanPath2 = b'W:\\SP\xed\x8c\x80\\\xed\x81\xac\xeb\xa3\xa8\xed\x94\x8c\xeb\x9e\x9c\\2022'.decode('utf-8')
        self.alpha = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.sheetDict = {
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
        self.setupUI()
        self.checkCsvPath()


    # UI.
    def setupUI(self):
        if pm.window('Crew_Plan', exists=True):
            pm.deleteUI('Crew_Plan')
        win = pm.window('Crew_Plan', t='Crew_Plan', s=True, rtf=True)
        pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=310)
        pm.separator(h=10)
        pm.button('Open csv file', c=lambda x: self.openCsv())
        self.csvField = pm.textField('csvField', ed=False)
        pm.separator(h=10)
        pm.rowColumnLayout(nc=4, cw=[(1, 95), (2, 55), (3, 90), (4, 60)])
        self.yearField = pm.optionMenu(l='Date : ')
        pm.menuItem(l='2022')
        self.monthField = pm.optionMenu(l='  -')
        mm = pm.date(f='MM')
        mm = int(mm) - 1
        mm = mm if mm else 12
        for k in range(mm):
            pm.menuItem(l='%d' % (mm - k))
        pm.text('Start column : ', al='right')
        self.columnField = pm.textField(ed=True)
        pm.setParent("..", u=True)
        pm.button('Overwrite', c=lambda x: self.crewPlanMain())
        pm.separator(h=10)
        pm.textField('resultField', ed=False) #, bgc=(1.052, 0.275, 0.204))
        pm.separator(h=10)
        pm.showWindow(win)


    def checkCsvPath(self):
        chk = os.path.isfile(self.myCrewPlanPath)
        if chk:
            with open(self.myCrewPlanPath, 'r') as file:
                line = file.readline()
                self.csvField.setText(line)
        else:
            self.csvField.setText("First run.")


    def writeCsv(self, fullPath):
        with open(self.myCrewPlanPath, 'w') as file:
            file.write(fullPath)


    def openCsv(self):
        csvPath = pm.fileDialog2(dir=self.myCrewPlanPath2, fm=0, ff='csv (*.csv);; All Files (*.*)')
        if csvPath:
            csvPath = ''.join(csvPath)
            self.csvField.setText(csvPath)
            file = os.path.basename(csvPath)
            name = file.split("_")[2]
            self.userName = name
            # Remember csv path.
            self.writeCsv(csvPath)
        else:
            self.csvField.setText('Canceled.')
            # self.csvField.setBackgroundColor(val=(1.052, 0.275, 0.204))


    def getDayCount(self, month):
        year = pm.date(f='YYYY')
        year = int(year)
        dayDict = {
            1: 31, 
            2: 28 if year%4 else 29, 
            3: 31, 
            4: 30, 
            5: 31, 
            6: 30, 
            7: 31, 
            8: 31, 
            9: 30, 
            10: 31, 
            11: 30, 
            12: 31
        }
        keys = dayDict.keys()
        keys = list(keys)
        if month in keys:
            return dayDict[month]
        else:
            return False


    def getCsvInfo(self):
        csv = self.csvField.getText()
        year = self.yearField.getValue()
        month = self.monthField.getValue()
        month = int(month)
        month = '%02d' % month
        date = f"{year}-{month}"
        with open(csv, 'r') as file:
            data = file.readlines()
        dataList = []
        for i in data:
            i = i.replace("\n", "")
            line = i.split(",")
            if line[2].startswith(date):
                dataList.append(line[2:7])
            else:
                continue
        # print(dataList)
        return dataList


    # Convert number to column character in excel.
    def numberToColumn(self, number):
        count = 0
        column = ''
        for j in itertools.count(1): # count(1) -> 'A', 'B' / count(2) -> 'AA', 'AB' / count(3) -> 'AAA', 'AAB'
            if count > number:
                break
            for k in itertools.product(self.alpha, repeat=j):
                count += 1
                if count > number:
                    # yield ''.join(k)
                    column = ''.join(k)
                    break
        return column


    # Convert column letters to numbers in Excel.
    def columnToNumber(self, column):
        count = 0
        isSame = False
        for j in itertools.count(1): # count(1) -> 'A', 'B' / count(2) -> 'AA', 'AB' / count(3) -> 'AAA', 'AAB'
            if isSame:
                break
            for k in itertools.product(self.alpha, repeat=j):
                if column == ''.join(k):
                    isSame = True
                    # yield count
                    break
                count += 1
        return count


    def crewPlanMain(self):
        data = self.getCsvInfo()
        column = self.columnField.getText()
        num = self.columnToNumber(column)
        month = self.monthField.getValue()
        month = int(month)
        day = self.getDayCount(month)
        userRow = '70'
        columnList = [self.numberToColumn(i) for i in range(num, num + day)]
        orgPath = 'C:/Users/jkhong/Desktop/크루플랜(2022)_v01.xlsx'
        loadExcel = openpyxl.load_workbook(orgPath)
        for i in data:
            date = i[0]
            date = date.split("-")[-1]
            date = int(date)
            idx = date - 1
            colRow = columnList[idx] + userRow
            sheetValue, cellValue = self.getInputData(i[1], i[2], i[3], i[4])
            sName = loadExcel[self.sheetDict[sheetValue]]
            sName[colRow] = float(cellValue) if cellValue.isdigit() else cellValue
        loadExcel.save(orgPath)


    def getInputData(self, sheet, time, sum, typ):
        if typ == '휴가':
            r_sheet = '기타'
            value = '0.0'
        elif typ == '반차':
            r_sheet = sheet
            value = '반' if sheet == '기타' and time == '0.0' else time
        elif typ == '정상근무':
            r_sheet = sheet
            value = time
        return r_sheet, value



        


crewPlan()