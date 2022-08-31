import maya.OpenMaya as om
import pymel.core as pm
import openpyxl
import os
import itertools


class crewPlan():
    def __init__(self):
        self.myCrewPlanPath = pm.internalVar(uad=True) + 'myCrewPlanPath.txt'
        self.wCrewPlanFolder = 'W:/SP팀/크루플랜/2022'
        # self.originalExcelFolder = "W:/SP팀/크루플랜/크루플랜(2022)_v01.xlsx"
        self.originalExcelFolder = 'C:/Users/jkhong/Desktop/크루플랜(2022)_v01.xlsx'
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
        win = pm.window('Crew_Plan', t='크루플랜 입력기', s=True, rtf=True)
        pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=310)
        pm.separator(h=10)
        pm.button('CSV 파일 열기', c=lambda x: self.openCsv())
        # my csv file path is here.
        self.csvField = pm.textField('csvField', ed=False)
        pm.separator(h=10)
        pm.rowColumnLayout(nc=4, cw=[(1, 95), (2, 55), (3, 90), (4, 60)])
        # This year.
        self.yearField = pm.optionMenu(l='날짜 : ')
        pm.menuItem(l='2022')
        # This month.
        self.monthField = pm.optionMenu(l='  -')
        mm = pm.date(f='MM')
        mm = int(mm)
        for k in range(1, mm + 1):
            pm.menuItem(l='%d' % (mm - k + 1))
        # Start column in of this month in excel File. ex) 6: FE, 7: GJ, 8: HP
        pm.text('이달의 시작 열 : ', al='right')
        self.columnField = pm.textField(ed=True, pht='FE, GJ, HP')
        self.nameText = pm.text(al='left')
        pm.text('    ')
        pm.text('사용자 시작 행 : ', al='right')
        self.userRowField = pm.textField(ed=True, pht=70)
        pm.setParent("..", u=True)
        pm.separator(h=10)
        self.OriginFile = pm.textField(ed=False)
        pm.button('원본 파일 열기', c=lambda x: self.openOrginalPath())
        pm.separator(h=10)
        pm.button('덮어쓰기', c=lambda x: self.crewPlanMain())
        pm.button('이번달 셀 초기화', c=lambda x: print('Not Ready.'))
        pm.separator(h=10)
        # This is alert messages.
        # self.alarm = pm.textField('resultField', ed=False) #, bgc=(1.052, 0.275, 0.204))
        # pm.separator(h=10)
        pm.showWindow(win)


    # To load paths automatically the next time you run the tool.
    def checkCsvPath(self):
        # Check this folder -> C:\Users\users\Documents\maya
        # Put the 'myCrewPlanPath.txt'
        chk = os.path.isfile(self.myCrewPlanPath)
        if chk:
            with open(self.myCrewPlanPath, 'r') as file:
                line = file.readline()
                self.csvField.setText(line)
                name = os.path.basename(line)
                name = name.split("_")[2]
                self.nameText.setLabel(f"이름 :   {name}")
        else:
            self.csvField.setText('')
            self.nameText.setLabel("이름 :   ")


    # Save the Crewplan folder path as txt in My Documents Maya folder.
    def writeCsv(self, fullPath):
        with open(self.myCrewPlanPath, 'w') as file:
            file.write(fullPath)


    # Open the csv file and save the path to the My Documents Maya folder.
    def openCsv(self):
        csvPath = pm.fileDialog2(dir=self.wCrewPlanFolder, fm=0, ff='csv (*.csv);; All Files (*.*)')
        if csvPath:
            csvPath = ''.join(csvPath)
            self.csvField.setText(csvPath)
            file = os.path.basename(csvPath)
            name = file.split("_")[2]
            self.nameText.setLabel(f"이름 :   {name}")
            # Remember csv path.
            self.writeCsv(csvPath)
        else:
            self.csvField.setText('')


    # Get the number of days in the this month. Calculate leap years.
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


    # Load information from csv file.
    # Return the information as a list.
    def getCsvInfo(self, csvPath):
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


    # Organize the data to put in the cell
    def getInputData(self, sheet, wTime, sum, typ):
        r_sheet = sheet
        value = wTime
        if typ == '휴가':
            r_sheet = '기타'
            value = '휴'
        elif typ == '반차':
            r_sheet = sheet
            value = '반' if sheet == '기타' and wTime == '0.0' else (float(wTime) / 8)
        elif typ == '정상근무':
            r_sheet = sheet
            value = float(wTime) / float(sum)
        elif typ == '기타':
            r_sheet = sheet
            value = float(wTime) / float(sum)
        else:
            om.MGlobal.displayError('휴가, 반차, 정상근무 이외의 항목이 있습니다.')
            r_sheet = ''
            value = 0
        return r_sheet, value


    # Open Original Excel File.
    def openOrginalPath(self):
        orgPath = pm.fileDialog2(dir=self.originalExcelFolder, fm=0, ff='xlsx (*.xlsx);; All Files (*.*)')
        if orgPath:
            orgPath = ''.join(orgPath)
            self.OriginFile.setText(orgPath)
        else:
            self.OriginFile.setText('')


    # Main Function.
    def crewPlanMain(self):
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


crewPlan()