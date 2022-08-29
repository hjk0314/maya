import pymel.core as pm
import openpyxl
import os


class crewPlan():
    def __init__(self):
        self.userName = ''
        self.myCrewPlanPath = pm.internalVar(uad=True) + 'myCrewPlanPath.txt'
        self.myCrewPlanPath2 = b'W:\\SP\xed\x8c\x80\\\xed\x81\xac\xeb\xa3\xa8\xed\x94\x8c\xeb\x9e\x9c\\2022'.decode('utf-8')
        self.alpha = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 
            'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 0
        }
        self.swap_alpha = {value: key for key, value in self.alpha.items()}
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


    def getColumn(self, number, base): # getColumn(224, 26) -> 'HP'
        print(number)
        baseList = []
        while number > 0:
            if number == 26:
                baseList.append('Z')
                break
            else:
                number, mod = divmod(number, base)
                baseList.append(self.swap_alpha[mod])
        result = baseList[::-1] # ['H', 'P']
        result = ''.join(result)
        return result # 'HP'


    def convertColumnToBase(self, columnString, base): # convertColumnToBase('HP', 26) -> 224
        columnList = list(columnString) # 'HP' -> ['H', 'P']
        columnList = columnList[::-1] # ['H', 'P'] -> ['P', 'H']
        result = 0
        for j, k in enumerate(columnList):
            result += self.alpha[k] * base ** j # 'P'*(base**j) + 'H'*(base**j)
        # print(result)
        return result


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


    def crewPlanMain(self):
        # data = self.getCsvInfo()
        column = self.columnField.getText()
        # print(type(column))
        decimal = self.convertColumnToBase(column, 26)
        # print(f"decimal : {decimal}")
        month = self.monthField.getValue()
        month = int(month)
        day = self.getDayCount(month)
        # print(day)
        userRow = '13'
        columnList = [self.getColumn(i, 26) for i in range(decimal, decimal + day)]
        print(columnList)
            # print(i)
            
        #     print(a)
        #     columnList.append(a)
        # for i in columnList:
        #     print(i)
        # print(len(columnList))
            
        




crewPlan()