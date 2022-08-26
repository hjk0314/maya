import pymel.core as pm
import openpyxl


class crewPlan():
    def __init__(self):
        self.setupUI()


    # UI.
    def setupUI(self):
        if pm.window('Crew_Plan', exists=True):
            pm.deleteUI('Crew_Plan')
        win = pm.window('Crew_Plan', t='Crew_Plan', s=True, rtf=True)
        pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=310)
        pm.separator(h=10)
        pm.text('__name__') #, bgc=(0.2, 0.2, 0.4))
        pm.separator(h=10)
        pm.button('Open csv file', c=lambda x: print(''))
        pm.separator(h=10)
        pm.rowColumnLayout(nc=4, cw=[(1, 95), (2, 55), (3, 90), (4, 60)])
        pm.optionMenu(l='Date : ', cc=print)
        pm.menuItem(l='2022')
        pm.optionMenu(l='  -', cc=print)
        mm = pm.date(f='MM')
        mm = int(mm) - 1
        mm = mm if mm else 12
        pm.menuItem(l='%d' % mm)
        pm.text('Start column : ', al='right')
        pm.textField(ed=True)
        pm.setParent("..", u=True)
        pm.separator(h=10)
        pm.button('Overwrite', c=lambda x: print(''))
        pm.separator(h=10)
        pm.text('__end__') #, bgc=(0.4, 0.2, 0.2))
        pm.separator(h=10)
        pm.showWindow(win)


    def crewPlan(self):
        csv = "C:/Users/jkhong/Desktop/ANI_Team_jkhong_data.csv"
        year = pm.date(f="YYYY")
        month = '%02d' % 8
        date = f"{year}-{month}"
        with open(csv, 'r') as file:
            data = file.readlines()
        dataHash = {}
        for i in data:
            i = i.replace("\n", "")
            line = i.split(",")
            if line[2].startswith(date):
                dataHash[line[2]] = line[2:7]
            else:
                continue
        print(dataHash)
        # excel = openpyxl.load_workbook('path')
        # sheet = excel['sheetName']
        # sheet['HP70'] = 1.0
        # excel.save('path')


crewPlan()