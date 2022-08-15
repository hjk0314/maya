# import maya.cmds as cmds
# import maya.OpenMaya as om
import pymel.core as pm
# import json
# import os


# Grouping itself and named own
def grp(cp=False):
    sel = pm.ls(sl=True)
    grpList = []
    for i in sel:
        grp = pm.group(i, n="%s_grp" % i)
        if not cp:
            pm.move(0, 0, 0, grp + ".scalePivot", grp + ".rotatePivot", rpr=True)
        grpList.append(grp)
    return grpList


# Create three types of locators.
# When you select two objects, a locator is created at the midpoint.
def loc():
    sel = pm.ls(sl=True)
    num = len(sel)
    if num == 1: # Select One point.
        position = pm.xform(sel[0], q=True, t=True, ws=True)
        position = tuple(position)
    elif num == 2: # Select Two points.
        twoPoint = [pm.xform(i, q=True, t=True, ws=True) for i in sel]
        position = tuple((twoPoint[0][i] + twoPoint[1][i]) / 2 for i in range(3))
    else:
        position = (0, 0, 0)
    loc = pm.spaceLocator(p=position)
    pm.xform(loc, t=position, ws=True)
    return position


# Create a curve controller.
def ctrl(cub=False, sph=False, cyl=False, pip=False, con=False, arr1=False, arr2=False, arr3=False, arr4=False, arr5=False):
    ctrl = {
    "cub": [
        (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), 
        (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), 
        (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), 
        (0.5, 0.5, 0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5)], 
    "sph": [
        (0.0, 1.0, 0.0), (0.0, 0.707, 0.707), (0.0, 0.0, 1.0), (0.0, -0.707, 0.707), (0.0, -1.0, 0.0), 
        (0.0, -0.707, -0.707), (0.0, 0.0, -1.0), (0.0, 0.707, -0.707), (0.0, 1.0, 0.0), (-0.707, 0.707, 0.0), 
        (-1.0, 0.0, 0.0), (-0.707, 0.0, 0.707), (0.0, 0.0, 1.0), (0.707, 0.0, 0.707), (1.0, 0.0, 0.0), 
        (0.707, 0.0, -0.707), (0.0, 0.0, -1.0), (-0.707, 0.0, -0.707), (-1.0, 0.0, 0.0), (-0.707, -0.707, 0.0), 
        (0.0, -1.0, 0.0), (0.707, -0.707, 0.0), (1.0, 0.0, 0.0), (0.707, 0.707, 0.0), (0.0, 1.0, 0.0)], 
    "cyl": [
        (-1.0, 1.0, 0.0), (-0.707, 1.0, 0.707), (0.0, 1.0, 1.0), (0.707, 1.0, 0.707), (1.0, 1.0, 0.0), 
        (0.707, 1.0, -0.707), (0.0, 1.0, -1.0), (0.0, 1.0, 1.0), (0.0, -1.0, 1.0), (-0.707, -1.0, 0.707), 
        (-1.0, -1.0, 0.0), (-0.707, -1.0, -0.707), (0.0, -1.0, -1.0), (0.707, -1.0, -0.707), (1.0, -1.0, 0.0), 
        (0.707, -1.0, 0.707), (0.0, -1.0, 1.0), (0.0, -1.0, -1.0), (0.0, 1.0, -1.0), (-0.7071, 1.0, -0.707), 
        (-1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0)], 
    "pip": [
        (0.0, 1.0, 1), (0.0, -1.0, 1), (0.707, -1.0, 0.707), (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (0.707, 1.0, -0.707), 
        (0.0, 1.0, -1), (0.0, -1.0, -1), (-0.707, -1.0, -0.707), (-1, -1.0, 0.0), (-1, 1.0, 0.0), (-0.707, 1.0, 0.707), 
        (0.0, 1.0, 1), (0.707, 1.0, 0.707), (1.0, 1.0, 0.0), (1.0, -1.0, 0.0), (0.707, -1.0, -0.707), (0.0, -1.0, -1), 
        (0.0, 1.0, -1), (-0.707, 1.0, -0.707), (-1, 1.0, 0.0), (-1, -1.0, 0.0), (-0.707, -1.0, 0.707), (0.0, -1.0, 1)], 
    "con": [
        (0.0, 2.0, 0.0), (-0.866, 0.0, -0.0), (0.866, 0.0, 0.0), (0.0, 2.0, 0.0), 
        (0.0, 0.0, 1.0), (-0.866, 0.0, -0.0), (0.866, 0.0, 0.0), (0.0, 0.0, 1.0)], 
    "arr1": [
        (1.0, 1.0, 0.0), (0.924, 1.0, -0.383), (0.707, 1.0, -0.707), (0.383, 1.0, -0.924), 
        (0, 1.0, -1.0), (0.226, 1.0, -1.075), (0.172, 1.0, -0.834), (0, 1.0, -1.0)], 
    "arr2": [
        (1.0, 1.0, 0.0), (0.866, 1.0, -0.5), (0.5, 1.0, -0.866), (0.0, 1.0, -1.0), (-0.5, 1.0, -0.866), 
        (-0.866, 1.0, -0.5), (-1.0, 1.0, 0.0), (-1.087, 1.0, -0.299), (-0.772, 1.0, -0.204), (-1.0, 1.0, 0.0)], 
    "arr3": [
        (0.866, 1.0, -0.5), (0.5, 1.0, -0.866), (0.0, 1.0, -1.0), (-0.5, 1.0, -0.866), (-0.866, 1.0, -0.5), 
        (-1.0, 1.0, 0.0), (-0.866, 1.0, 0.5), (-0.5, 1.0, 0.866), (0.0, 1.0, 1.0), (0.5, 1.0, 0.866), 
        (0.866, 1.0, 0.5), (0.949, 1.0, 0.19), (0.949, 1.0, 0.19), (0.816, 1.0, 0.15), (1.0, 1.0, 0.0), 
        (1.086, 1.0, 0.231), (0.949, 1.0, 0.19)], 
    "arr4": [
        (0.0, 0.0, 2.0), (2.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 0.0, -2.0), 
        (-1.0, 0.0, -2.0), (-1.0, 0.0, 1.0), (-2.0, 0.0, 1.0), (0.0, 0.0, 2.0)], 
    "arr5": [
        (0.0, 0.5, 2.0), (2.0, 0.5, 1.0), (1.0, 0.5, 1.0), (1.0, 0.5, -2.0), (-1.0, 0.5, -2.0), (-1.0, 0.5, 1.0), 
        (-2.0, 0.5, 1.0), (0.0, 0.5, 2.0), (0.0, -0.5, 2.0), (2.0, -0.5, 1.0), (1.0, -0.5, 1.0), (1.0, -0.5, -2.0), 
        (-1.0, -0.5, -2.0), (-1.0, -0.5, 1.0), (-2.0, -0.5, 1.0), (0.0, -0.5, 2.0), (2.0, -0.5, 1.0), (2.0, 0.5, 1.0), 
        (1.0, 0.5, 1.0), (1.0, 0.5, -2.0), (1.0, -0.5, -2.0), (-1.0, -0.5, -2.0), (-1.0, 0.5, -2.0), (-1.0, 0.5, 1.0), 
        (-2.0, 0.5, 1.0), (-2.0, -0.5, 1.0)]
    }
    shapeList = []
    if cub: shapeList.append("cub")
    if sph: shapeList.append("sph")
    if cyl: shapeList.append("cyl")
    if pip: shapeList.append("pip")
    if con: shapeList.append("con")
    if arr1: shapeList.append("arr1")
    if arr2: shapeList.append("arr2")
    if arr3: shapeList.append("arr3")
    if arr4: shapeList.append("arr4")
    if arr5: shapeList.append("arr5")
    if shapeList:
        for i in shapeList:
            pm.curve(d=1, p=ctrl[i])
    else:
        shapes = list(ctrl.keys())
        print(f"Shape's List: {shapes}")


class rename():
    def __init__(self):
        self.setupUI()


    # UI.
    def setupUI(self):
        if pm.window('Re_name', exists=True):
            pm.deleteUI('Re_name')
        else:
            win = pm.window('Re_name', t='rename', s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=391)
            pm.separator(h=10)
            self.new = pm.textFieldGrp(l="New name : ", ed=True)
            self.chk = pm.checkBoxGrp(l='Replace : ', ncb=1, v1=False, cc=lambda x: self.setUI())
            self.rep = pm.textFieldGrp(l="Replace to this : ", ed=True, en=False)
            self.end = pm.textFieldGrp(l="End : ", ed=True, tcc=lambda x: self.setUI())
            self.btn = pm.button(l='New', c=lambda x: self.reName())
            pm.separator(h=10)
            pm.showWindow(win)
    

    def setUI(self):
        chk = self.chk.getValue1()
        end = '' if chk else self.end.getText()
        newlbl = "Find : " if chk else "New name : "
        btnlbl = "Rename" if chk else "New"
        self.end.setText(end)
        self.new.setLabel(newlbl)
        self.btn.setLabel(btnlbl)
        self.new.setEnable(not end)
        self.rep.setEnable(chk)
        self.end.setEnable(not chk)


    # The number is last one in name.
    # This function is Only works for strings sliced with underscores.
    # Return index and its number.
    def getNumberInName(self, name): # input example : 'pCube1_22_obj_22_a2'
        nameSlice = name.split("_") # ['pCube1', '22', 'obj', '22', 'a2']
        digitList = [(j, k) for j, k in enumerate(nameSlice) if k.isdigit()] # [(1, '22'), (3, '22')]
        try:
            idx, num = digitList[-1]
            return idx, int(num)
        except:
            return False


    def reName(self):
        sel = pm.ls(sl=True)
        chk = self.chk.getValue1()
        new = self.new.getText()
        print(new)
        if chk:
            rep = self.rep.getText()
            for i in sel:
                pm.rename(i, i.replace(new, rep))
        else:
            end = self.end.getText()
            for i in sel:
                pm.rename(i, i + end if end else new)


