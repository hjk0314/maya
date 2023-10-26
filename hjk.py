import re
import os
import json
import shutil
import math
import sympy
import functools
import maya.OpenMaya as om
import pymel.core as pm
import maya.mel as mel
import pathlib


class SoftSel:
    def __init__(self):
        """ Get this code from internet. Modified to class. """
        self.createSoftCluster()
    
    
    def softSelection(self):
        selection = om.MSelectionList()
        softSelection = om.MRichSelection()
        om.MGlobal.getRichSelection(softSelection)
        softSelection.getSelection(selection)
        dagPath = om.MDagPath()
        component = om.MObject()
        iter = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
        elements = []
        while not iter.isDone(): 
            iter.getDagPath(dagPath, component)
            dagPath.pop()
            node = dagPath.fullPathName()
            fnComp = om.MFnSingleIndexedComponent(component)   
            for i in range(fnComp.elementCount()):
                elem = fnComp.element(i)
                infl = fnComp.weight(i).influence()
                elements.append([node, elem, infl])
            iter.next()
        return elements

    def createSoftCluster(self):
        softElementData = self.softSelection()
        selection = ["%s.vtx[%d]" % (el[0], el[1]) for el in softElementData] 
        pm.select(selection, r=True)
        cluster = pm.cluster(relative=True)
        for i in range(len(softElementData)):
            pm.percent(cluster[0], selection[i], v=softElementData[i][2])
        pm.select(cluster[1], r=True)


class Han:
    def __init__(self):
        """ Transform HanGeul unicode to bytes. Otherside too. """
        self.btnHan1 = b'\xec\x9d\xb8\xec\xbd\x94\xeb\x94\xa9'
        self.btnHan2 = b'\xec\xa7\x80\xec\x9a\xb0\xea\xb8\xb0'
        self.HanGeul = b'\xed\x95\x9c\xea\xb8\x80'
        self.setupUI()


    # UI.
    def setupUI(self):
        if pm.window('HanGeul', exists=True):
            pm.deleteUI('HanGeul')
        else:
            win = pm.window('HanGeul', t='Encode / Decode', s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=240)
            pm.separator(h=10)
            self.hanField = pm.textField(ed=True, pht=self.HanGeul)
            self.utfField = pm.textField(ed=True, pht="Bytes")
            self.btn = pm.button(l=self.btnHan1, c=lambda x: self.transform())
            pm.separator(h=10)
            pm.showWindow(win)


    # The field value is returned as a string type.
    def transform(self):
        A = self.hanField.getText()
        B = self.utfField.getText()
        if A and not B:
            result = r"%s" % (str(A).encode("utf-8"))
            self.utfField.setText(result)
            self.btn.setLabel(self.btnHan2)
        elif B and not A:
            result = eval(B)
            self.hanField.setText(result.decode("utf-8", "strict"))
            self.btn.setLabel(self.btnHan2)
        else:
            self.hanField.setText("")
            self.utfField.setText("")
            self.btn.setLabel(self.btnHan1)


class AutoWheel_Rig2:
    def __init__(self, arg=None):
        self.sel = self.checkParam(arg)
        self.main()


    def main(self):
        for obj in self.sel:
            ctrl = self.createWheelCtrl(obj)
            offGrp = self.createOffsetGrp(ctrl)
            loc = self.createCtrlLocator(ctrl)
            null, prev, orient = self.createGroupNames(offGrp)
            self.createCtrlChannel(ctrl)
            self.createOffsetChannel(offGrp)
            self.createCtrlGroup(offGrp, null, prev, orient)
            self.createExpression(ctrl, offGrp, loc, orient, prev)


    def checkParam(self, obj):
        if obj and isinstance(obj, list):
            for j, k in enumerate(obj):
                if isinstance(k, pm.PyNode):
                    continue
                else:
                    obj[j] = pm.PyNode(k)
            result = obj
        else:
            result = pm.ls(sl=True)
        return result


    def createWheelCtrl(self, obj, sizeUp=1.2):
        bb = pm.xform(obj, q=True, bb=True, ws=True)
        xMin, yMin, zMin, xMax, yMax, zMax = bb
        x = (xMax - xMin) / 2
        y = (yMax - yMin) / 2
        z = (zMax - zMin) / 2
        rad = max(x, y, z)
        rad = round(rad, 3) * sizeUp
        cuv = pm.circle(nr=(1, 0, 0), r=rad, n=f"cc_{obj}", ch=False)
        cuv = cuv[0]
        pm.matchTransform(cuv, obj, pos=True)
        return cuv


    def createOffsetGrp(self, obj):
        result = pm.group(obj, n=f"{obj}_offset")
        pm.xform(result, os=True, piv=(0,0,0))
        return result


    def createCtrlLocator(self, ctrl):
        loc = pm.spaceLocator(n='loc_' + ctrl)
        pm.matchTransform(loc, ctrl, pos=True)
        pm.parent(loc, ctrl)
        return loc


    def createGroupNames(self, offset):
        null = offset + '_null_grp'
        prev = offset + '_prev_grp'
        orient = offset + '_orient_grp'
        return null, prev, orient


    def createCtrlChannel(self, ctrl):
        # Creates a Radius channel.
        attrRad = "Radius"
        pm.addAttr(ctrl, ln=attrRad, at='double', min=0.0001, dv=1)
        pm.setAttr(f'{ctrl}.{attrRad}', e=True, k=True)
        # Creates a AutoRoll channel.
        attrAuto = 'AutoRoll'
        pm.addAttr(ctrl, ln=attrAuto, at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{ctrl}.{attrAuto}', e=True, k=True)


    def createOffsetChannel(self, offset):
        # Creates a PrePos channel.
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(offset, ln=f'PrevPos{i}', at='double', dv=0)
            pm.setAttr(f'{offset}.PrevPos{i}', e=True, k=True)


    def createCtrlGroup(self, offset, null, prev, orient):
        if not offset.getParent():
            tempGrp = pm.group(em=True)
            pm.parent(offset, tempGrp)
        pm.group(n=null, em=True, p=offset)
        pm.group(n=prev, em=True, p=offset.getParent())
        print("createCtrlGroup Done.")
        ort = pm.group(n=orient, em=True, p=prev)
        pos = [-0.001, -0.001, -0.001]
        ort.translate.set(pos)
        pm.aimConstraint(offset, prev, mo=False)
        pm.orientConstraint(null, orient, mo=False)


    def createExpression(self, ctrl, offset, loc, orient, prev):
        br = '\n'
        # expression1
        expr1 = f'float $R = {ctrl}.Radius;{br}'
        expr1 += f'float $A = {ctrl}.AutoRoll;{br}'
        expr1 += f'float $J = {loc}.rotateX;{br}'
        expr1 += f'float $C = 2 * 3.141 * $R;{br}'
        expr1 += f'float $O = {orient}.rotateY;{br}'
        expr1 += f'float $S = {offset}.scaleY;{br}'
        expr1 += f'float $pX = {offset}.PrevPosX;{br}'
        expr1 += f'float $pY = {offset}.PrevPosY;{br}'
        expr1 += f'float $pZ = {offset}.PrevPosZ;{br}'
        expr1 += f'{prev}.translateX = $pX;{br}'
        expr1 += f'{prev}.translateY = $pY;{br}'
        expr1 += f'{prev}.translateZ = $pZ;{br}'
        expr1 += f'float $nX = {offset}.translateX;{br}'
        expr1 += f'float $nY = {offset}.translateY;{br}'
        expr1 += f'float $nZ = {offset}.translateZ;{br*2}'
        # expression2
        expr2 = f'float $D = `mag<<$nX-$pX, $nY-$pY, $nZ-$pZ>>`;{br*2}'
        # expression3
        expr3 = f'{loc}.rotateX = $J'
        expr3 += ' + ($D/$C) * 360'
        expr3 += ' * $A'
        expr3 += ' * 1'
        expr3 += ' * sin(deg_to_rad($O))'
        expr3 += f' / $S;{br*2}'
        # expression4
        expr4 = f'{offset}.PrevPosX = $nX;{br}'
        expr4 += f'{offset}.PrevPosY = $nY;{br}'
        expr4 += f'{offset}.PrevPosZ = $nZ;{br}'
        # final
        expr = expr1 + expr2 + expr3 + expr4
        pm.expression(s=expr, o='', ae=1, uc='all')


class AutoRig_Wheel:
    def __init__(self, arg=None):
        """ Automatically creates rigging 
        to turn your selection into wheels. Or, 
        insert the controller's list as a parameter.
        Constraint the wheel to the locator, 
        The movement of the wheel is connected to the offset group.
         """
        self.sel = self.checkParam(arg)
        self.main()


    def main(self):
        """ 1. First, create a controller.
        2. Create a parent group for the controller.
        3. Create a locator under the controller.
        4. Name several groups.
        5. Create the Radius and AutoRoll channels of the controller.
        6. Setting relationships with groups.
        7. Finally, create an expression.
         """
        for obj in self.sel:
            ctrl = self.createWheelCtrl(obj)
            off = self.createOffsetGrp(ctrl)
            loc = self.createCtrlLocator(ctrl)
            null, prev, orient = self.createGroupNames(off)
            self.createCtrlChannel(ctrl)
            self.createOffsetChannel(off)
            self.createCtrlGroup(off, null, prev, orient)
            self.createExpression(ctrl, off, loc, orient, prev)


    def checkParam(self, obj):
        """ Checks if there is an argument 
        and creates the argument as PyNode.
         """
        if obj and isinstance(obj, list):
            for j, k in enumerate(obj):
                if isinstance(k, pm.PyNode):
                    continue
                else:
                    obj[j] = pm.PyNode(k)
            result = obj
        else:
            result = pm.ls(sl=True)
        return result


    def createWheelCtrl(self, obj, sizeUp=1.2):
        """ Create a controller 1.2 times larger than 
        the boundingBox size of the selected object.
         """
        bb = pm.xform(obj, q=True, bb=True, ws=True)
        xMin, yMin, zMin, xMax, yMax, zMax = bb
        x = (xMax - xMin) / 2
        y = (yMax - yMin) / 2
        z = (zMax - zMin) / 2
        rad = max(x, y, z)
        rad = round(rad, 3) * sizeUp
        cuv = pm.circle(nr=(1, 0, 0), r=rad, n=f"cc_{obj}", ch=False)
        cuv = cuv[0]
        pm.matchTransform(cuv, obj, pos=True)
        return cuv


    def createOffsetGrp(self, obj):
        """ Create a parent group for the controller. """
        result = pm.group(obj, n=f"{obj}_offset")
        pm.xform(result, os=True, piv=(0,0,0))
        return result


    def createCtrlLocator(self, ctrl):
        """ Place the locator under the controller. """
        loc = pm.spaceLocator(n='loc_' + ctrl)
        pm.matchTransform(loc, ctrl, pos=True)
        pm.parent(loc, ctrl)
        return loc


    def createGroupNames(self, offset):
        """ Create another group name. """
        null = offset + '_null_grp'
        prev = offset + '_prev_grp'
        orient = offset + '_orient_grp'
        return null, prev, orient


    def createCtrlChannel(self, ctrl):
        """ Creates a Radius channel and AutoRoll channel. """
        attrRad = "Radius"
        pm.addAttr(ctrl, ln=attrRad, at='double', min=0.0001, dv=1)
        pm.setAttr(f'{ctrl}.{attrRad}', e=True, k=True)
        attrAuto = 'AutoRoll'
        pm.addAttr(ctrl, ln=attrAuto, at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{ctrl}.{attrAuto}', e=True, k=True)


    def createOffsetChannel(self, offset):
        """ Create a PrePos channel in the offset group. """
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(offset, ln=f'PrevPos{i}', at='double', dv=0)
            pm.setAttr(f'{offset}.PrevPos{i}', e=True, k=True)


    def createCtrlGroup(self, offset, null, prev, orient):
        """ Determine group relationships. """
        if offset.getParent():
            pm.parent(offset, offset.getParent())
        else:
            tempGrp = pm.group(em=True)
            pm.parent(offset, tempGrp)
        pm.group(n=null, em=True, p=offset)
        pm.group(n=prev, em=True, p=offset.getParent())
        ort = pm.group(n=orient, em=True, p=prev)
        pos = [-0.001, -0.001, -0.001]
        ort.translate.set(pos)
        pm.aimConstraint(offset, prev, mo=False)
        pm.orientConstraint(null, orient, mo=False)


    def createExpression(self, ctrl, offset, loc, orient, prev):
        """ Create an expression. """
        br = '\n'
        # expression1
        expr1 = f'float $R = {ctrl}.Radius;{br}'
        expr1 += f'float $A = {ctrl}.AutoRoll;{br}'
        expr1 += f'float $J = {loc}.rotateX;{br}'
        expr1 += f'float $C = 2 * 3.141 * $R;{br}'
        expr1 += f'float $O = {orient}.rotateY;{br}'
        expr1 += f'float $S = {offset}.scaleY;{br}'
        expr1 += f'float $pX = {offset}.PrevPosX;{br}'
        expr1 += f'float $pY = {offset}.PrevPosY;{br}'
        expr1 += f'float $pZ = {offset}.PrevPosZ;{br}'
        expr1 += f'{prev}.translateX = $pX;{br}'
        expr1 += f'{prev}.translateY = $pY;{br}'
        expr1 += f'{prev}.translateZ = $pZ;{br}'
        expr1 += f'float $nX = {offset}.translateX;{br}'
        expr1 += f'float $nY = {offset}.translateY;{br}'
        expr1 += f'float $nZ = {offset}.translateZ;{br*2}'
        # expression2
        expr2 = f'float $D = `mag<<$nX-$pX, $nY-$pY, $nZ-$pZ>>`;{br*2}'
        # expression3
        expr3 = f'{loc}.rotateX = $J'
        expr3 += ' + ($D/$C) * 360'
        expr3 += ' * $A'
        expr3 += ' * 1'
        expr3 += ' * sin(deg_to_rad($O))'
        expr3 += f' / $S;{br*2}'
        # expression4
        expr4 = f'{offset}.PrevPosX = $nX;{br}'
        expr4 += f'{offset}.PrevPosY = $nY;{br}'
        expr4 += f'{offset}.PrevPosZ = $nZ;{br}'
        # final
        expr = expr1 + expr2 + expr3 + expr4
        pm.expression(s=expr, o='', ae=1, uc='all')


class AutoWheel_Rig:
    def __init__(self, arg: list=None):
        sel = arg if arg else pm.ls(sl=True)
        self.ccDict = {}
        for i in sel:
            cc = pm.PyNode(i)
            offset = pm.group(i, n=f"{i}_offset")
            pm.xform(offset, os=True, piv=(0,0,0))
            self.ccDict[cc] = offset
        self.main()
            

    def main(self):
        for ctrl, offset in self.ccDict.items():
            var = self.createVariables(ctrl, offset)
            self.createCtrlChannel(ctrl, offset)
            self.createCtrlGroup(offset, var)
            self.createExpression(offset, var)


    def createCtrlChannel(self, ctrl, offset):
        # Creates a Radius channel.
        attrRad = "Radius"
        pm.addAttr(ctrl, ln=attrRad, at='double', min=0.0001, dv=1)
        pm.setAttr(f'{ctrl}.{attrRad}', e=True, k=True)
        # Creates a AutoRoll channel.
        attrAuto = 'AutoRoll'
        pm.addAttr(ctrl, ln=attrAuto, at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{ctrl}.{attrAuto}', e=True, k=True)
        # Creates a PrePos channel.
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(offset, ln=f'PrevPos{i}', at='double', dv=0)
            pm.setAttr(f'{offset}.PrevPos{i}', e=True, k=True)


    def createCtrlGroup(self, offset, var):
        null, prev, orient, expr = var
        pm.group(n=null, em=True, p=offset)
        pm.group(n=prev, em=True, p=offset.getParent())
        ort = pm.group(n=orient, em=True, p=prev)
        pos = [-0.001, -0.001, -0.001]
        ort.translate.set(pos)


    def createExpression(self, offset, var):
        null, prev, orient, expr = var
        pm.aimConstraint(offset, prev, mo=False)
        pm.orientConstraint(null, orient, mo=False)
        pm.expression(s=expr, o='', ae=1, uc='all')


    def createCtrlLocator(self, ctrl):
        loc = pm.spaceLocator(n='loc_' + ctrl)
        pm.matchTransform(loc, ctrl, pos=True)
        pm.parent(loc, ctrl)
        return loc


    def createVariables(self, ctrl, offset):
        loc = self.createCtrlLocator(ctrl)
        null = offset + '_null_grp'
        prev = offset + '_prev_grp'
        orient = offset + '_orient_grp'
        br = '\n'
        # expression1 ==================================================
        expr1 = f'float $R = {ctrl}.Radius;{br}'
        expr1 += f'float $A = {ctrl}.AutoRoll;{br}'
        expr1 += f'float $J = {loc}.rotateX;{br}'
        expr1 += f'float $C = 2 * 3.141 * $R;{br}' # 2*pi*r
        expr1 += f'float $O = {orient}.rotateY;{br}'
        expr1 += f'float $S = {offset}.scaleY;{br}' # Connect the global scale.
        expr1 += f'float $pX = {offset}.PrevPosX;{br}'
        expr1 += f'float $pY = {offset}.PrevPosY;{br}'
        expr1 += f'float $pZ = {offset}.PrevPosZ;{br}'
        expr1 += f'{prev}.translateX = $pX;{br}'
        expr1 += f'{prev}.translateY = $pY;{br}'
        expr1 += f'{prev}.translateZ = $pZ;{br}'
        expr1 += f'float $nX = {offset}.translateX;{br}'
        expr1 += f'float $nY = {offset}.translateY;{br}'
        expr1 += f'float $nZ = {offset}.translateZ;{br*2}'
        # expression2: Distance between two points.
        expr2 = f'float $D = `mag<<$nX-$pX, $nY-$pY, $nZ-$pZ>>`;{br*2}'
        # expression3: Insert value into jonit rotation.
        expr3 = f'{loc}.rotateX = $J' # Original rotation value.
        expr3 += ' + ($D/$C) * 360' # Proportional: (d / 2*pi*r) * 360
        expr3 += ' * $A' # Auto roll switch.
        expr3 += ' * 1' # Create other switches.
        expr3 += ' * sin(deg_to_rad($O))' # When the wheel turns.
        expr3 += f' / $S;{br*2}' # Resizing the global scale.
        # expression4
        expr4 = f'{offset}.PrevPosX = $nX;{br}'
        expr4 += f'{offset}.PrevPosY = $nY;{br}'
        expr4 += f'{offset}.PrevPosZ = $nZ;{br}'
        # expression Final =============================================
        expr = expr1 + expr2 + expr3 + expr4
        # Result
        result = [null, prev, orient, expr]
        return result


class AutoWheel_Key:
    def __init__(self):
        """ Set the key on the wheel to turn automatically. """
        self.Min = pm.playbackOptions(q=True, min=True)
        self.Max = pm.playbackOptions(q=True, max=True)
        self.setupUI()


    def setupUI(self):
        if pm.window('AutoWheel2', exists=True):
            pm.deleteUI('AutoWheel2')
        else:
            title = "Set the key on the wheel to turn automatically."
            win = pm.window('AutoWheel2', t=title, s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=210)
            pm.separator(h=10)
            pm.rowColumnLayout(nc=4, cw=[(1, 55), (2, 50), (3, 15), (4, 50)])
            pm.text("Frame : ")
            self.startF = pm.intField("startFrame", ed=True, v=self.Min)
            pm.text(" - ")
            self.endF = pm.intField("endFrame", v=self.Max)
            pm.setParent("..", u=True)
            pm.button(l='Auto Rotation', c=lambda x: self.main())
            pm.button(l='Delete Key', c=lambda x: self.deleteKey())
            pm.separator(h=10)
            pm.showWindow(win)
    

    def main(self):
        sel = pm.ls(sl=True)
        radiusCheck = []
        for i in sel:
            attrCheck = pm.attributeQuery('Radius', node=i, ex=True)
            if not attrCheck:
                radiusCheck.append(i)
        if not sel:
            print("Nothing Selected.")
        elif radiusCheck:
            print("The controller does not have a radius attribute.")
        else:
            for i in sel:
                self.autoRotate(i)


    def autoRotate(self, obj):
        startFrame = self.startF.getValue()
        endFrame = self.endF.getValue()
        rad = pm.getAttr(f"{obj}.Radius")
        size = pm.xform(obj, q=True, s=True, ws=True)
        size = max(size)
        pointList = {}
        for i in range(startFrame, endFrame + 1):
            pm.currentTime(i)
            pm.setKeyframe(at="rotateX")
            pos = pm.xform(obj, q=True, ws=True, rp=True)
            pos = [round(j, 3) for j in pos]
            pointList[i] = pos
            if len(pointList) < 2:
                continue
            else:
                x1, y1, z1 = pointList[i - 1]
                x2, y2, z2 = pointList[i]
                dx = x2 - x1
                dy = y2 - y1
                dz = z2 - z1
                d = math.sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2))
                d = round(d, 3)
                pm.currentTime(i - 1)
                angle = pm.getAttr(f"{obj}.rotateX")
                angle += d * 360 / (2 * 3.14159 * rad * size)
                pm.currentTime(i)
                pm.setKeyframe(obj, v=angle, at="rotateX")


    def deleteKey(self):
        sel = pm.ls(sl=True)
        startFrame = self.startF.getValue()
        endFrame = self.endF.getValue()
        for i in sel:
            pm.cutKey(i, cl=True, at="rx", t=(startFrame, endFrame))
        

class MatchPivot:
    def __init__(self):
        """ Matching the direction of the pivot using 3points. """
        self.main()


    # Check if selected is a point.
    def check(self, sel: list) -> bool:
        vtxList = [i for i in sel if isinstance(i, pm.MeshVertex)]
        if not sel:
            om.MGlobal.displayError('Nothing selected.')
            result = False
        elif len(sel) != 3 or len(vtxList) != 3:
            om.MGlobal.displayError('Select 3 points.')
            result = False
        else:
            result = True
        return result


    # Decide the direction.
    # Input is a list of 3 points.
    def select3Points(self, sel: list) -> str:
        # shp: shape
        shp = sel[0].split('.')[0]
        # Object's name
        obj = pm.listRelatives(shp, p=True)
        obj = obj[0]
        # pPlane's name
        pPlane = pm.polyPlane(sx=1, sy=1, ax=(0, 1, 0), cuv=2, ch=False)
        pPlane = pPlane[0]
        vtx = pm.ls(f"{pPlane}.vtx[0:2]", fl=True)
        all = vtx + sel
        pm.select(all)
        mel.eval("snap3PointsTo3Points(0);")
        pm.select(cl=True)
        return pPlane

    
    def main(self) -> None:
        sel = pm.ls(sl=True, fl=True)
        chk = self.check(sel)
        if not chk:
            pass
        else:
            obj = self.select3Points(sel)
            loc = pm.spaceLocator()
            pm.matchTransform(loc, obj, pos=True, rot=True)
            pm.delete(obj)


class MatchCuvShp:
    def __init__(self):
        """ Match the curve shape from A to B.
        Select only nurbsCurves. """
        self.main()


    # Number of Object's cv.
    def numberOfCV(self, obj: str) -> int:
        cv = f'{obj}.cv[0:]'
        pm.select(cv)
        cvSel = pm.ls(sl=True, fl=True)
        cvNum = len(cvSel)
        result = cvNum
        pm.select(cl=True)
        return result

        
    # Match the point to point.
    # Change the shape of the curve controller from A to B
    def matchShape(self, obj: list) -> list:
        A_list = obj[0:-1]
        B = obj[-1] # The last selection is Base.
        numB = self.numberOfCV(B) # number of B.cv
        failed = []
        for A in A_list:
            numA = self.numberOfCV(A)
            if numA == numB > 0:
                for k in range(numA):
                    cvA = f'{A}.cv[{k}]'
                    cvB = f'{B}.cv[{k}]'
                    p1, p2, p3 = pm.pointPosition(cvB)
                    pm.move(p1, p2, p3, cvA, a=True)
            else:
                failed.append(A)
        return failed


    # Select at least 2.
    def main(self):
        sel = pm.ls(sl=True, dag=True, type=['nurbsCurve'])
        if len(sel) < 2:
            print('Select two or more "nurbsCurves".')
        else:
            result = self.matchShape(sel)
            failed = 'Check this objects : %s' % result
            success = 'Successfully done.'
            message = failed if result else success
            print(message)


class MirrorCopy:
    def __init__(self, **kwargs):
        """ Parameter can be (x=True or z=True).
        First Select groups.
        Copy the group and mirror it in the direction. 
        If there is a curve in it, copy the curve and mirror it.
         """
        if not kwargs:
            print("Parameter is required. ex) x=True or z=True")
            return
        keys = [i for i in kwargs.keys() if i == ('x' or 'z')]
        keys = [i for i in keys if kwargs[i]]
        if not keys:
            print("None of the parameters are True.")
        else:
            self.key = keys[0]
            self.val = kwargs[self.key]
            self.sel = pm.ls(sl=True)
            self.main()


    # Check the conditions.
    def main(self):
        if not self.sel:
            print("Nothing selected.")
            return
        for i in self.sel:
            self.mirrorCopy(i)


    # If there is a curve in the group, copy the curve and mirror it.
    def mirrorCopy(self, selection):
        cuv = selection.getChildren()
        shp = pm.ls(cuv, dag=True, s=True)
        typ = 'nurbsCurve'
        objs = {i.getParent().name() for i in shp if pm.objectType(i)==typ}
        objs = list(objs)
        if not objs:
            self.mirrorGroup(selection)
        else:
            for obj in objs:
                name = self.swapLR(obj)
                copy = pm.duplicate(obj, rr=True, n=name)
                pm.parent(copy, w=True)
                grp = pm.group(em=True)
                pm.parent(copy, grp)
                direction = [-1, 1, 1] if self.key=='x' else [1, 1, -1]
                pm.scale(grp, direction, r=True)
                mirrorGrp = self.mirrorGroup(selection)
                pm.parent(copy, mirrorGrp)
                pm.makeIdentity(copy, a=True, t=1, r=1, s=1, n=0, pn=1)
                pm.delete(grp)
        

    # Replace letter L with R
    def swapLR(self, objName):
        if '_L' in objName:
            result = objName.replace('_L', '_R')
        elif '_R' in objName:
            result = objName.replace('_R', '_L')
        else:
            result = ''
        return result


    # Create a mirrored group.
    def mirrorGroup(self, selection):
        name = self.swapLR(selection.name())
        grp = pm.group(em=True, n=name)
        pm.matchTransform(grp, selection, pos=True, rot=True)
        tra = pm.getAttr(f'{grp}.translate')
        rot = pm.getAttr(f'{grp}.rotate')
        tx, ty, tz = tra
        rx, ry, rz = rot
        if self.key == 'x':
            tx *= -1
            rx += (180 if rx < 0 else -180)
            ry *= -1
            rz *= -1
        else:
            tz *= -1
            rz += (180 if rz < 0 else -180)
        attr = {'tx': tx, 'ty': ty, 'tz': tz, 'rx': rx, 'ry': ry, 'rz': rz}
        for j, k in attr.items():
            pm.setAttr(f'{grp}.{j}', k)
        return grp


class VertexSeletor:
    def __init__(self):
        """ Save the selected vertices, lines and faces, 
        to json files in the same path of this scene.
         """
        self.jsonPath = self.getJsonPath()
        if not self.jsonPath:
            return
        else:
            self.setupUI()
    

    def getJsonPath(self):
        """ Create the path of the json file based on this scene. """
        fullPath = pm.Env().sceneName()
        if not fullPath:
            print("File not saved.")
            return
        else:
            dir = os.path.dirname(fullPath)
            # name_ext = os.path.basename(fullPath)
            # name, ext = os.path.splitext(name_ext)
            result = f"{dir}/vertexSeletor.json"
            return result


    # UI
    def setupUI(self):
        winName = 'vertexButton'
        if pm.window(winName, exists=True):
            pm.deleteUI(winName)
        win = pm.window(winName, t='Vertex Selector', s=True, rtf=True)
        pm.columnLayout(cat=('both', 4), rs=2, cw=178)
        pm.separator(h=10)
        pm.rowColumnLayout(nc=3, cw=[(1, 80), (2, 5), (3, 80)])
        self.field = pm.textField(ed=True)
        pm.text('')
        pm.button(l="Create", c=lambda x: self.writeJson())
        pm.setParent("..", u=True)
        pm.separator(h=10)
        pm.rowColumnLayout(nc=3, cw=[(1, 80), (2, 5), (3, 80)])
        pm.radioCollection()
        self.radioAdd = pm.radioButton(l='add', sl=True)
        pm.text('')
        self.radioTgl = pm.radioButton(l='tgl')
        pm.setParent("..", u=True)
        spacing = [(1, 80), (2, 3), (3, 80), (4, 3)]
        pm.rowColumnLayout(nc=4, rs=(1, 3), cw=spacing)
        chk = os.path.isfile(self.jsonPath)
        if chk:
            data = self.loadJson()
            for key in data:
                self.button(key)
        else:
            pass
        pm.setParent("..", u=True)
        pm.separator(h=10)
        pm.button(l="Clear", c=lambda x: pm.select(cl=True))
        pm.button(l="Delete Data", c=lambda x: self.deleteJson())
        pm.button(l="Close", c=lambda x: pm.deleteUI(winName))
        pm.separator(h=10)
        pm.showWindow(win)


    def button(self, *args):
        """ Create the looping button. """
        for i in args:
            pm.button(l=i, c=lambda x: self.selectVtx(i))
            pm.text(' ')


    def writeJson(self) -> None:
        """ If the json file does not exist, create a new one.
        Otherwise, Save the dictionary as a json file
         """
        chk = os.path.isfile(self.jsonPath)
        if not chk:
            data = {}
        else:
            data = self.loadJson()
        name = self.field.getText()
        info = self.vertexNum()
        data[name] = info
        with open(self.jsonPath, 'w') as JSON:
            json.dump(data, JSON, indent=4)
        VertexSeletor()


    def loadJson(self) -> dict:
        """ Load information from json file and select vertex. """
        with open(self.jsonPath, 'r') as JSON:
            data = json.load(JSON)
        return data


    def deleteJson(self):
        """ It doesn't delete the data, it destroys the file itself. """
        chk = os.path.isfile(self.jsonPath)
        if not chk:
            return
        else:
            os.remove(self.jsonPath)


    def vertexNum(self) -> dict:
        """ Make a list of vertex numbers only. """
        sel = pm.ls(sl=True)
        obj = pm.ls(sel, o=True)
        shapes = set(obj)
        result = {}
        for shp in shapes:
            com = re.compile(f'(?<={shp}).+[0-9]+:*[0-9]*.+')
            vtxNum = []
            for j in sel:
                try:
                    tmp = com.search(j.name())
                    vtxNum.append(tmp.group(0))
                except:
                    continue
            result[shp.getParent().name()] = vtxNum
        return result


    def selectVtx(self, key: str):
        """ Click the button, selects the vortex. """
        data = self.loadJson()
        temp = data[key]
        result = []
        for j, k in temp.items():
            for i in k:
                result.append(j + i)
        ADD = self.radioAdd.getSelect()
        TGL = self.radioTgl.getSelect()
        pm.select(result, af=ADD, tgl=TGL)


class LineConnect:
    def __init__(self):
        """ Creates a line connecting two objects or two points.
        If you select a point initially, 
        the last one you select must also be a point. 
        If you have selected an object, you must select the object last.
        input() is where you put the name of the line..
         """
        self.sel = pm.ls(sl=True, fl=True)
        try:
            self.name = input()
        except:
            print("Cancled.")
            return
        self.main()


    def main(self):
        """ Make a line first. 
        Create an expression that calculates the distance between two points, 
        and create a channel to write it. 
        Connect each with pointConstraint and aimConstraint. 
        upVector is used for aimConstraint.
         """
        if not self.sel:
            print("Nothing selected.")
        elif len(self.sel) < 2:
            print("Two points are needed.")
        else:
            # cuv: curve
            # cuvLen: length of curve
            # aloc: start object or point
            # oloc: last object or point
            # grp: group of curve
            # upV: up vector of the curve
            cuv, aloc, oloc = self.makeLine()
            cuvLen = pm.arclen(cuv)
            cuvLen = round(cuvLen, 3)
            self.makeAttr(cuv)
            self.makeExression(aloc, oloc, cuv, cuvLen)
            grp = self.makeGroup(cuv)
            upV = self.makeUpVector(cuv, grp)
            self.makeConstraint(aloc, oloc, cuv, upV)


    # Create a line connecting two points.
    def makeLine(self) -> str:
        alpha = self.sel[0]
        omega = self.sel[-1]
        try:
            aPos, oPos = [pm.pointPosition(i) for i in [alpha, omega]]
        except:
            tmp = []
            for i in [alpha, omega]:
                pos = pm.xform(i, q=1, ws=1, rp=1)
                tmp.append(pos)
            aPos, oPos = tmp
        cuv = pm.curve(d=1, p=[aPos, oPos], n=self.name)
        sPiv = f"{cuv}.scalePivot"
        rPiv = f"{cuv}.rotatePivot"
        aLoc = pm.spaceLocator(n=f"{cuv}_startLoc")
        oLoc = pm.spaceLocator(n=f"{cuv}_endLoc")
        a1, a2, a3 = aPos
        o1, o2, o3 = oPos
        pm.move(a1, a2, a3, aLoc, r=True)
        pm.move(o1, o2, o3, oLoc, r=True)
        pm.move(a1, a2, a3, sPiv, rPiv, rpr=True)
        pm.aimConstraint(oLoc, aLoc)
        pm.delete(aLoc, cn=True)
        pm.parent(cuv, aLoc)
        pm.makeIdentity(cuv, a=True, t=1, r=1, s=1, n=0, pn=1)
        pm.parent(cuv, w=True)
        pm.rebuildCurve(cuv, d=1, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)
        pm.xform(cuv, cpc=True)
        return cuv, aLoc, oLoc


    # create attr to curve
    def makeAttr(self, cuv):
        for attrName in ['Distance', 'Ratio']:
            pm.addAttr(cuv, ln=attrName, at='double', dv=0)
            pm.setAttr(f'{cuv}.{attrName}', e=True, k=True)


    # create expression to curve attr
    def makeExression(self, Loc1, Loc2, cuv, cuvLen):
        BR = "\n"
        expr = f"float $uX = {Loc1}.translateX;" + BR
        expr += f"float $uY = {Loc1}.translateY;" + BR
        expr += f"float $uZ = {Loc1}.translateZ;" + BR
        expr += f"float $dX = {Loc2}.translateX;" + BR
        expr += f"float $dY = {Loc2}.translateY;" + BR
        expr += f"float $dZ = {Loc2}.translateZ;" + BR
        expr += "float $D = `mag<<$dX-$uX, $dY-$uY, $dZ-$uZ>>`;" + BR
        expr += f"{cuv}.Distance = $D;" + BR
        expr += f"{cuv}.Ratio = $D / {cuvLen};"
        pm.expression(s=expr, o='', ae=1, uc='all')


    # create group
    def makeGroup(self, obj):
        grp = pm.group(em=True, n=f"{obj}_grp")
        pm.matchTransform(grp, obj, pos=True, rot=True)
        pm.parent(obj, grp)
        return grp


    # create upVector
    def makeUpVector(self, cuv, grp):
        locUpVector = pm.spaceLocator(n=f'{cuv}_upVector')
        length = pm.getAttr(f"{cuv}.Distance")
        pm.matchTransform(locUpVector, cuv, pos=True, rot=True)
        pm.parent(locUpVector, grp)
        pm.move(0, length, 0, locUpVector, r=True, ls=True, wd=True)
        # pm.parent(locUpVector, w=True)
        return locUpVector


    # The line is centered between the two points.
    def makeConstraint(self, Loc1, Loc2, cuv, upVector):
        up = upVector.name(long=True)
        pm.pointConstraint(Loc1, cuv, mo=True, w=0.5)
        pm.pointConstraint(Loc2, cuv, mo=True, w=0.5)
        pm.aimConstraint(Loc2, cuv, wut="object", wuo=up)
        for i in ["sx", "sy", "sz"]:
            pm.connectAttr(f"{cuv}.Ratio", f"{cuv}.{i}")


class Colors:
    def __init__(self):
        """ Change the color of the shape. """
        self.setupUI()


    # UI
    def setupUI(self):
        winName = 'colorsButton'
        if pm.window(winName, exists=True):
            pm.deleteUI(winName)
        else:
            win = pm.window(winName, t='Colors', s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=188)
            pm.separator(h=10)
            pm.rowColumnLayout(nc=2, cw=[(1, 90), (2, 90)])
            pm.button(l='colors_blue', c=lambda x: self.colors("blue"))
            pm.button(l='colors_blue2', c=lambda x: self.colors("blue2"))
            pm.button(l='colors_pink', c=lambda x: self.colors("pink"))
            pm.button(l='colors_red', c=lambda x: self.colors("red"))
            pm.button(l='colors_red2', c=lambda x: self.colors("red2"))
            pm.button(l='colors_green', c=lambda x: self.colors("green"))
            pm.button(l='colors_green2', c=lambda x: self.colors("green2"))
            pm.button(l='colors_yellow', c=lambda x: self.colors("yellow"))
            pm.setParent("..", u=True)
            pm.separator(h=10)
            pm.button(l="Close", c=lambda x: pm.deleteUI(winName))
            pm.separator(h=10)
            pm.showWindow(win)


    # This is Main function.
    def colors(self, arg=None):
        tmp = {}
        if arg == None:
            print("arg is None.")
            return
        elif isinstance(arg, str):
            sel = pm.ls(sl=True)
            tmp[arg] = sel
            print(tmp)
        elif isinstance(arg, dict):
            tmp = arg
        else:
            return
        pallette = {
            "blue": 6, 
            "blue2": 18, 
            "pink": 9, 
            "red": 13, 
            "red2": 21, 
            "green": 14, 
            "green2": 23, 
            "yellow": 17, 
        }
        for color, objList in tmp.items():
            idx = pallette[color]
            enb = 1 if idx else 0
            for obj in objList:
                obj = pm.PyNode(obj)
                shp = obj.getShape()
                pm.setAttr(f"{shp}.overrideEnabled", enb)
                pm.setAttr(f"{shp}.overrideColor", idx)


class SolariBoard:
    def __init__(self):
        """ A Class to create a solariBoard. 
        Select the cards in order and call this function. 
        Enter the <name of the controller> in the "input() window". 
        The number of cards must be 5 or more. 
        Use setRange node, plusMinusEverage node and expression. 
        Cards turned upside down can be problematic.
         """
        self.main()


    # main Function
    def main(self):
        ctrlName = self.inputCtrl()
        if not ctrlName:
            print("No Controllers.")
            return
        self.createChannel(ctrlName)
        ctrl = ctrlName[0]
        sel = pm.ls(sl=True)
        num = len(sel)
        if num < 5:
            print("The minimum number must be 5 or more.")
        else:
            keyNode = self.createKeyNode(ctrl, num)
            seR = self.setRangeNodes(num)
            plM = self.plusMinusNodes(num)
            self.connectNodes(keyNode, sel, seR, plM)
            self.createExpression(sel)


    # If there is no channel named "Var" in the controller, create one.
    def createChannel(self, ctrlName: list) -> None:
        channelName = "Var"
        for i in ctrlName:
            chk = pm.attributeQuery(f'{channelName}', node=i, ex=True)
            if chk:
                continue
            else:
                pm.addAttr(i, ln=f'{channelName}', at='float', dv=0, min=0)
                pm.setAttr(f'{i}.{channelName}', e=True, k=True)


    # Handling when nothing is entered into the input() window.
    def inputCtrl(self) -> list:
        try:
            inp = input()
        except:
            inp = ''
        result = pm.ls(inp)
        return result


    # To make the card repeat, we create a new looping animCurve.
    def createKeyNode(self, ctrl: str, num: int) -> str:
        startFrame = 0
        endFrame = num
        endValue = num
        pm.setKeyframe(ctrl, at="Var", t=startFrame, v=startFrame)
        pm.setKeyframe(ctrl, at="Var", t=endFrame, v=endValue)
        keyNode = pm.listConnections(ctrl, scn=True)[0]
        pm.selectKey(keyNode, add=True, k=True, t=(startFrame, endFrame))
        pm.keyTangent(itt="linear", ott="linear")
        pm.setInfinity(poi="cycle")
        pm.disconnectAttr(f"{keyNode}.output", f"{ctrl}.Var")
        pm.connectAttr(f"{ctrl}.Var", f"{keyNode}.input", f=True)
        return keyNode


    # Process the value passed from the setRange node.
    def plusMinusNodes(self, num: int) -> list:
        node = "plusMinusAverage"
        result = [pm.shadingNode(node, au=True) for i in range(num)]
        return result


    def setRangeNodes(self, num: int) -> list:
        """ Create a setRange node. 
        The end of the setRange node is unusual.
          """
        result = []
        for i in range(num):
            tmp = pm.shadingNode("setRange", au=True)
            if i != (num - 1):
                pm.setAttr(f"{tmp}.maxX", 180)
                pm.setAttr(f"{tmp}.maxY", 180)
                pm.setAttr(f"{tmp}.maxZ", 180)
                pm.setAttr(f"{tmp}.oldMinX", i)
                pm.setAttr(f"{tmp}.oldMinY", i + 1)
                pm.setAttr(f"{tmp}.oldMinZ", i + 2)
                pm.setAttr(f"{tmp}.oldMaxX", i + 1)
                pm.setAttr(f"{tmp}.oldMaxY", i + 2)
                pm.setAttr(f"{tmp}.oldMaxZ", i + 3)
            else:
                pm.setAttr(f"{tmp}.minX", 180)
                pm.setAttr(f"{tmp}.maxX", 360)
                pm.setAttr(f"{tmp}.maxY", 180)
                pm.setAttr(f"{tmp}.maxZ", 180)
                pm.setAttr(f"{tmp}.oldMinX", i)
                pm.setAttr(f"{tmp}.oldMinY", 0)
                pm.setAttr(f"{tmp}.oldMinZ", 1)
                pm.setAttr(f"{tmp}.oldMaxX", i + 1)
                pm.setAttr(f"{tmp}.oldMaxY", 1)
                pm.setAttr(f"{tmp}.oldMaxZ", 2)
            result.append(tmp)
        return result


    def connectNodes(self, ctrl, objs, seRnodes, plMnodes):
        """ Connect nodes.
        animCurve -> setRange 
        setRange -> plusMinusEverage 
        plusMinusEverage -> object's rotate
         """
        for i, obj in enumerate(objs):
            seR = seRnodes[i]
            plM = plMnodes[i]
            pm.connectAttr(f"{ctrl}.output", f"{seR}.valueX", f=True)
            pm.connectAttr(f"{ctrl}.output", f"{seR}.valueZ", f=True)
            pm.connectAttr(f"{seR}.outValueX", f"{plM}.input1D[0]", f=True)
            pm.connectAttr(f"{seR}.outValueZ", f"{plM}.input1D[1]", f=True)
            pm.connectAttr(f"{plM}.output1D", f"{obj}.rotateX", f=True)


    # There are five types of expression.
    def createExpression(self, sel):
        num = len(sel)
        # The minimum number must be 5 or more.
        if num < 5:
            return
        _1st = sel[0]
        _2nd = sel[1]
        _end = sel[-2]
        last = sel[-1]
        for j, k in enumerate(sel):
            rotX = "rotateX"
            vis = "visibility"
            if j == 0:
                expr = f"if (({_1st}.{rotX} == 0) || "
                expr += f"({_1st}.{rotX} == 180)) {_1st}.{vis} = 1;\n"
                expr += f"if ({_1st}.{rotX} == 360) {_1st}.{vis} = 0;\n"
                expr += f"if ({last}.{rotX} > 360) {_1st}.{vis} = 1;\n"
                expr += f"if ({_2nd}.{rotX} == 180) {_1st}.{vis} = 0;\n"
            elif j == 1:
                expr = f"if ({_2nd}.{rotX} == 0) {_2nd}.{vis} = 0;\n"
                expr += f"if ({_1st}.{rotX} > 0) {_2nd}.{vis} = 1;\n"
                expr += f"if ({sel[j+1]}.{rotX} == 180) {_2nd}.{vis} = 0;\n"
                expr += f"if ({_2nd}.{rotX} == 360) {_2nd}.{vis} = 0;\n"
            elif j == (num - 2):
                expr = f"if ({_end}.{rotX} == 0) {_end}.{vis} = 0;\n"
                expr += f"if ({sel[j-1]}.{rotX} > 0) {_end}.{vis} = 1;\n"
                expr += f"if ({last}.{rotX} == 540) {_end}.{vis} = 0;\n"
            elif j == (num - 1):
                expr = f"if ({last}.{rotX} == 180) {last}.{vis} = 1;\n"
                expr += f"if ({last}.{rotX} == 360) {last}.{vis} = 0;\n"
                expr += f"if ({_1st}.{rotX} == 180) {last}.{vis} = 0;\n"
                expr += f"if ({_end}.{rotX} > 0) {last}.{vis} = 1;\n"
            else:
                expr = f"if (({k}.{rotX} == 0) || "
                expr += f"({k}.{rotX} == 360)) {k}.{vis} = 0;\n"
                expr += f"if (({sel[j-1]}.{rotX} > 0) && "
                expr += f"({sel[j-1]}.{rotX} < 360)) {k}.{vis} = 1;\n"
                expr += f"if ({sel[j+1]}.{rotX} == 180) {k}.{vis} = 0;\n"
            pm.expression(s=expr, o='', ae=1, uc='all')


def createCuv_thruPoint(startFrame: int, endFrame: int) -> list:
    """ Creates a curve through points.
    This function works even if you select a point.
     """
    sel = pm.ls(sl=True, fl=True)
    result = []
    for j in sel:
        pos = []
        for k in range(startFrame, endFrame + 1):
            pm.currentTime(k)
            try:
                pos.append(pm.pointPosition(j)) # vertex
            except:
                pos.append(pm.xform(j, q=1, ws=1, rp=1)) # object
        cuv = pm.curve(p=pos, d=3)
        result.append(cuv)
    return result


def createCuv_thruLoc(**kwargs) -> str:
    """ Creates a curve along the locator's points.
    Place locators first, and select them, and call this function.
    ex) cl=True -> Create a closed curve.
     """
    sel = pm.ls(sl=True) # select locators
    pos = [pm.xform(i, q=1, ws=1, rp=1) for i in sel]
    tmp = kwargs['cl'] if 'cl' in kwargs.keys() else False
    if tmp:
        cuv = pm.circle(nr=(0, 1, 0), ch=False, s=len(sel))
        cuv = cuv[0]
        for j, k in enumerate(pos):
            pm.move(k[0], k[1], k[2], f'{cuv}.cv[{j}]', ws=True)
    else:
        cuv = pm.curve(d=3, ep=pos)
    return cuv


def createLoc(**kwargs):
    """ Creates locator or joint in boundingBox.
    Usage: createLoc(jnt=True) """
    sel = pm.ls(sl=True)
    bb = pm.xform(sel, q=True, bb=True, ws=True)
    xMin, yMin, zMin, xMax, yMax, zMax = bb
    x = (xMin + xMax) / 2
    y = (yMin + yMax) / 2
    z = (zMin + zMax) / 2
    loc = pm.spaceLocator()
    pm.move(loc, x, y, z)
    if not kwargs:
        pass
    else:
        for key, value in kwargs.items():
            if key=="jnt" and value:
                pm.select(cl=True)
                jnt = pm.joint(p=(0,0,0), rad=1)
                pm.matchTransform(jnt, loc, pos=True)
                pm.delete(loc)
            else:
                continue


def createLine() -> str:
    """ Create a line connecting two points. """
    sel = pm.ls(sl=True, fl=True)
    if len(sel) < 2:
        print("Two points are needed.")
    else:
        alpha = sel[0]
        omega = sel[-1]
        try:
            aPos, oPos = [pm.pointPosition(i) for i in [alpha, omega]]
        except:
            aPos, oPos = [pm.xform(i, q=1, ws=1, rp=1) for i in [alpha, omega]]
        cuv = pm.curve(d=1, p=[aPos, oPos])
        sPiv = f"{cuv}.scalePivot"
        rPiv = f"{cuv}.rotatePivot"
        aLoc = pm.spaceLocator()
        oLoc = pm.spaceLocator()
        a1, a2, a3 = aPos
        o1, o2, o3 = oPos
        pm.move(a1, a2, a3, aLoc, r=True)
        pm.move(o1, o2, o3, oLoc, r=True)
        pm.move(a1, a2, a3, sPiv, rPiv, rpr=True)
        pm.aimConstraint(oLoc, aLoc)
        pm.delete(aLoc, cn=True)
        pm.parent(cuv, aLoc)
        pm.makeIdentity(cuv, a=True, t=1, r=1, s=1, n=0, pn=1)
        pm.parent(cuv, w=True)
        pm.rebuildCurve(cuv, d=1, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)
        return cuv


def createCircle(name: str, size: float, **kwargs) -> str:
    """ Create a circle.
    1. The circle name, 
    2. Size
    3. Normal direction
    -> createCircle("name", 3, x=True)
     """
    normal = {
        "x": (1, 0, 0), 
        "y": (0, 1, 0), 
        "z": (0, 0, 1), 
    }
    if not kwargs:
        axis = (0, 1, 0)
    else:
        for k, v in kwargs.items():
            if not k in normal.keys():
                axis = (0, 1, 0)
                continue
            elif not v:
                axis = (0, 1, 0)
                continue
            else:
                axis = normal[k]
    cuv = pm.circle(nr=axis, n=name, ch=False, r=size)[0]
    # pm.scale(cuv, [size, size, size])
    # pm.makeIdentity(cuv, a=True, n=0)
    return cuv


def createJnt_MotionPath(*arg: int) -> None:
    '''Create a number of joints and 
    apply a motionPath to the curve.
    '''
    sel = pm.ls(sl=True)
    if not sel:
        print("No curves selected.")
        return 0
    num = arg[0] if arg else int(input())
    mod = 1/(num-1) if num > 1 else 0
    cuv = sel[0]
    for i in range(num):
        pm.select(cl=True)
        jnt = pm.joint(p=(0,0,0))
        val = i * mod
        tmp = pm.pathAnimation(jnt, c=cuv, 
            fm=True, # fractionMode
            f=True, # follow
            fa='x', # followAxis
            ua='y', # upAxis
            wut='vector', # worldUpType
            wu=(0,1,0) # worldUpVector
            )
        pm.cutKey(tmp, cl=True, at='u')
        pm.setAttr(f"{tmp}.uValue", val)


def ctrl(*args: dict, **kwargs):
    """ Create a controller,
    "cub": cub, 
    "sph": sph, 
    "cyl": cyl, 
    "pip": pip, 
    "con1": con1, 
    "con2" : con2, 
    "car": car, 
    "car2": car2, 
    "car3": car3, 
    "ar1": ar1, 
    "ar2": ar2, 
    "ar3": ar3, 
    "ar4": ar4, 
    "ar5": ar5, 
    "pointer": pointer, 
    "foot": foot, 
    "foot2": foot2, 
    "hoof": hoof, 
    "hoof2": hoof2, 
    "sqr": sqr, 
    "cross": cross, 
    "hat": hat, 
    "head": head, 
    "scapula": scapula, 
     """
    # Cube
    cub = [(-1, 1, -1), (-1, 1, 1), (1, 1, 1), ]
    cub += [(1, 1, -1), (-1, 1, -1), (-1, -1, -1), ]
    cub += [(-1, -1, 1), (1, -1, 1), (1, -1, -1), ]
    cub += [(-1, -1, -1), (-1, -1, 1), (-1, 1, 1), ]
    cub += [(1, 1, 1), (1, -1, 1), (1, -1, -1), ]
    cub += [(1, 1, -1), ]
    # Sphere
    sph = [(0, 1, 0), (0, 0.7, 0.7), (0, 0, 1), ]
    sph += [(0, -0.7, 0.7), (0, -1, 0), (0, -0.7, -0.7), ]
    sph += [(0, 0, -1), (0, 0.7, -0.7), (0, 1, 0), ]
    sph += [(-0.7, 0.7, 0), (-1, 0, 0), (-0.7, 0, 0.7), ]
    sph += [(0, 0, 1), (0.7, 0, 0.7), (1, 0, 0), ]
    sph += [(0.7, 0, -0.7), (0, 0, -1), (-0.7, 0, -0.7), ]
    sph += [(-1, 0, 0), (-0.7, -0.7, 0), (0, -1, 0), ]
    sph += [(0.7, -0.7, 0), (1, 0, 0), (0.7, 0.7, 0), ]
    sph += [(0, 1, 0), ]
    # Cylinder
    cyl = [(-1, 1, 0), (-0.7, 1, 0.7), (0, 1, 1), ]
    cyl += [(0.7, 1, 0.7), (1, 1, 0), (0.7, 1, -0.7), ]
    cyl += [(0, 1, -1), (0, 1, 1), (0, -1, 1), ]
    cyl += [(-0.7, -1, 0.7), (-1, -1, 0), (-0.7, -1, -0.7), ]
    cyl += [(0, -1, -1), (0.7, -1, -0.7), (1, -1, 0), ]
    cyl += [(0.7, -1, 0.7), (0, -1, 1), (0, -1, -1), ]
    cyl += [(0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), ]
    cyl += [(1, 1, 0), (1, -1, 0), (-1, -1, 0), ]
    cyl += [(-1, 1, 0), ]
    # Pipe
    pip = [(0, 1, 1), (0, -1, 1), (0.7, -1, 0.7), ]
    pip += [(1, -1, 0), (1, 1, 0), (0.7, 1, -0.7), ]
    pip += [(0, 1, -1), (0, -1, -1), (-0.7, -1, -0.7), ]
    pip += [(-1, -1, 0), (-1, 1, 0), (-0.7, 1, 0.7), ]
    pip += [(0, 1, 1), (0.7, 1, 0.7), (1, 1, 0), ]
    pip += [(1, -1, 0), (0.7, -1, -0.7), (0, -1, -1), ]
    pip += [(0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), ]
    pip += [(-1, -1, 0), (-0.7, -1, 0.7), (0, -1, 1), ]
    # Cone1
    con1 = [(0, 2, 0), (-0.87, 0, -0), (0.87, 0, 0), ]
    con1 += [(0, 2, 0), (0, 0, 1), (-0.87, 0, -0), ]
    con1 += [(0.87, 0, 0), (0, 0, 1), ]
    # Cone2
    con2 = [(-1, 0, -0), (-0, 0, 1), (1, 0, 0), ]
    con2 += [(0, 0, -1), (-1, 0, -0), (0, 2, 0), ]
    con2 += [(-0, 0, 1), (1, 0, 0), (0, 2, 0), ]
    con2 += [(0, 0, -1), (0, 0, -1), (-1, 0, -0), ]
    con2 += [(-0, 0, 1), (1, 0, 0), (0, 2, 0)]
    # car
    car = [(81, 70, 119), (89, 56, 251), (89, -12, 251), ]
    car += [(89, -12, 117), (89, -12, -117), (89, -12, -229), ]
    car += [(81, 70, -229), (81, 70, -159), (69, 111, -105), ]
    car += [(69, 111, 63), (81, 70, 119), (-81, 70, 119), ]
    car += [(-89, 56, 251), (-89, -12, 251), (-89, -12, 117), ]
    car += [(-89, -12, -117), (-89, -12, -229), (-81, 70, -229), ]
    car += [(-81, 70, -159), (-69, 111, -105), (69, 111, -105), ]
    car += [(81, 70, -159), (-81, 70, -159), (-81, 70, -229), ]
    car += [(81, 70, -229), (89, -12, -229), (-89, -12, -229), ]
    car += [(-89, -12, -117), (-89, -12, 117), (-89, -12, 251), ]
    car += [(89, -12, 251), (89, 56, 251), (-89, 56, 251), ]
    car += [(-81, 70, 119), (-69, 111, 63), (-69, 111, -105), ]
    car += [(69, 111, -105), (69, 111, 63), (-69, 111, 63), ]
    # car2
    car2 = [(165, 0, -195), (0, 0, -276), (-165, 0, -195), ]
    car2 += [(-97, 0, -0), (-165, -0, 195), (-0, -0, 276), ]
    car2 += [(165, -0, 195), (97, -0, 0), (165, 0, -195), ]
    # Car3
    car3 = [(212, 0, -212), (0, 0, -300), (-212, 0, -212), ]
    car3 += [(-300, 0, 0), (-212, 0, 212), (0, 0, 300), ]
    car3 += [(212, 0, 212), (300, 0, 0), (212, 0, -212), ]
    # Arrow1
    ar1 = [(0, 0, 2), (2, 0, 1), (1, 0, 1), ]
    ar1 += [(1, 0, -2), (-1, 0, -2), (-1, 0, 1), ]
    ar1 += [(-2, 0, 1), (0, 0, 2), ]
    # Arrow2
    ar2 = [(0, 1, 4), (4, 1, 2), (2, 1, 2), ]
    ar2 += [(2, 1, -4), (-2, 1, -4), (-2, 1, 2), ]
    ar2 += [(-4, 1, 2), (0, 1, 4), (0, -1, 4), ]
    ar2 += [(4, -1, 2), (2, -1, 2), (2, -1, -4), ]
    ar2 += [(-2, -1, -4), (-2, -1, 2), (-4, -1, 2), ]
    ar2 += [(0, -1, 4), (4, -1, 2), (4, 1, 2), ]
    ar2 += [(2, 1, 2), (2, 1, -4), (2, -1, -4), ]
    ar2 += [(-2, -1, -4), (-2, 1, -4), (-2, 1, 2), ]
    ar2 += [(-4, 1, 2), (-4, -1, 2), ]
    # Arrow3
    ar3 = [(7, 0, 0), (5, 0, -5), (0, 0, -7), ]
    ar3 += [(-5, 0, -5), (-7, 0, 0), (-5, 0, 5), ]
    ar3 += [(0, 0, 7), (5, 0, 5), (7, 0, 0), ]
    ar3 += [(5, 0, 2), (7, 0, 3), (7, 0, 0), ]
    # Arrow4
    ar4 = [(0, 0, -11), (-3, 0, -8), (-2.0, 0, -8), ]
    ar4 += [(-2, 0, -6), (-5, 0, -5), (-6, 0, -2), ]
    ar4 += [(-8, 0, -2), (-8, 0, -3), (-11, 0, 0), ]
    ar4 += [(-8, 0, 3), (-8, 0, 2), (-6, 0, 2), ]
    ar4 += [(-5, 0, 5), (-2, 0, 6), (-2, 0, 8), ]
    ar4 += [(-3, 0, 8), (0, 0, 11), (3, 0, 8), ]
    ar4 += [(2, 0, 8), (2, 0, 6), (5, 0, 5), ]
    ar4 += [(6, 0, 2), (8, 0, 2), (8, 0, 3), ]
    ar4 += [(11, 0, 0), (8, 0, -3), (8, 0, -2), ]
    ar4 += [(6, 0, -2), (5, 0, -5), (2, 0, -6), ]
    ar4 += [(2, 0, -8), (3, 0, -8), (0, 0, -11), ]
    # Arrow5
    ar5 = [(-2, 0, -1), (2, 0, -1), (2, 0, -2), ]
    ar5 += [(4, 0, 0), (2, 0, 2), (2, 0, 1), ]
    ar5 += [(-2, 0, 1), (-2, 0, 2), (-4, 0, 0), ]
    ar5 += [(-2, 0, -2), (-2, 0, -1), ]
    # Arrow6
    ar6 = [(-6.3, 6, 0), (-6.5, 4, 0), (-5, 5, 0)]
    ar6 += [(-6.3, 6, 0), (-6, 5, 0), (-5, 3, 0)]
    ar6 += [(-3, 1, 0), (0, 0, 0), (3, 1, 0)]
    ar6 += [(5, 3, 0), (6, 5, 0), (6.3, 6, 0)]
    ar6 += [(5, 5, 0), (6.5, 4, 0), (6.3, 6, 0), ]
    # Pointer
    pointer = [(-1, 0, 0), (-0.7, 0, 0.7), (0, 0, 1), ]
    pointer += [(0.7, 0, 0.7), (1, 0, 0), (0.7, 0, -0.7), ]
    pointer += [(0, 0, -1), (-0.7, 0, -0.7), (-1, 0, 0), ]
    pointer += [(0, 0, 0), (0, 2, 0), ]
    # Foot
    foot = [(-4, 0, -4), (-4, 0, -7), (-3, 0, -11), ]
    foot += [(-1, 0, -12), (0, 0, -12), (1, 0, -12), ]
    foot += [(3, 0, -11), (4, 0, -7), (4, 0, -4), ]
    foot += [(-4, 0, -4), (-5, 0, 1), (-5, 0, 6), ]
    foot += [(-4, 0, 12), (-2, 0, 15), (0, 0, 15.5), ]
    foot += [(2, 0, 15), (4, 0, 12), (5, 0, 6), ]
    foot += [(5, 0, 1), (4, 0, -4), (-4, 0, -4), ]
    foot += [(4, 0, -4), ]
    # foot2
    foot2 = [(-6, 12, -14), (-6, 12, 6), (6, 12, 6), ]
    foot2 += [(6, 12, -14), (-6, 12, -14), (-6, 0, -14), ]
    foot2 += [(-6, 0, 18), (6, 0, 18), (6, 0, -14), ]
    foot2 += [(-6, 0, -14), (-6, 0, 18), (-6, 12, 6), ]
    foot2 += [(6, 12, 6), (6, 0, 18), (6, 0, -14), (6, 12, -14), ]
    # Hoof
    hoof = [(-6, 0, -5), (-6.5, 0, -1), (-6, 0, 3), ]
    hoof += [(-5.2, 0, 5.5), (-3, 0, 7.5), (0, 0, 8.2), ]
    hoof += [(3, 0, 7.5), (5.2, 0, 5.5), (6, 0, 3), ]
    hoof += [(6.5, 0, -1), (6, 0, -5), (4, 0, -5), ]
    hoof += [(4.5, 0, -1), (4, 0, 3), (3.5, 0, 4.5), ]
    hoof += [(2, 0, 6), (0, 0, 6.5), (-2, 0, 6), ]
    hoof += [(-3.5, 0, 4.5), (-4, 0, 3), (-4.5, 0, -1), ]
    hoof += [(-4, 0, -5), (-6, 0, -5), (-5.5, 0, -6.5), ]
    hoof += [(5.5, 0, -6.5), (4.5, 0, -10), (2.2, 0, -12.2), ]
    hoof += [(0, 0, -12.2), (-2.2, 0, -12.2), (-4.5, 0, -10), ]
    hoof += [(-5.5, 0, -6.5), ]
    # Hoof2
    hoof2 = [(6, 6, -12), (0, 8, -12), (-6, 6, -12), ]
    hoof2 += [(-8, 3, -13), (-8, 0, -12), (-7, 0, -10), ]
    hoof2 += [(-8, 0, -6), (-9, 0, -1), (-8, 0, 4), ]
    hoof2 += [(-5, 0, 9), (0, 0, 10), (5, 0, 9), ]
    hoof2 += [(8, 0, 4), (9, 0, -1), (8, 0, -6), ]
    hoof2 += [(7, 0, -10), (8, 0, -12), (8, 3, -13), ]
    hoof2 += [(6, 6, -12), ]
    # Square
    sqr = [(1, 0, 1), (1, 0, -1), (-1, 0, -1), ]
    sqr += [(-1, 0, 1), (1, 0, 1)]
    # Cross
    cross = [(0, 5, 1), (0, 5, -1), (0, 1, -1), ]
    cross += [(0, 1, -5), (0, -1, -5), (0, -1, -1), ]
    cross += [(0, -5, -1), (0, -5, 1), (0, -1, 1), ]
    cross += [(0, -1, 5), (0, 1, 5), (0, 1, 1), ]
    cross += [(0, 5, 1), ]
    # hat
    hat = [(14, 9, 0), (0, 15, 0), (-14, 9, 0), ]
    hat += [(-7, -5, 0), (-29, -7, 0), (0, -7, 0), ]
    hat += [(29, -7, 0), (7, -5, 0), (14, 9, 0), ]
    # head
    head = [(13, 15, -11), (0, 25, -15), (-13, 15, -11), ]
    head += [(-14, 6, 0), (-13, 15, 11), (0, 25, 15), ]
    head += [(13, 15, 11), (14, 6, 0), (13, 15, -11), ]
    # scapula
    scapula = [(2, 10, -11), (0, 0, -11), (-2, 10, -11), ]
    scapula += [(-3, 18, 0), (-2, 10, 11), (0, 0, 11), ]
    scapula += [(2, 10, 11), (3, 18, 0), (2, 10, -11), ]
    # Dictionary
    ctrl = {
        "cub": cub, 
        "sph": sph, 
        "cyl": cyl, 
        "pip": pip, 
        "con1": con1, 
        "con2": con2, 
        "car": car, 
        "car2": car2, 
        "car3": car3, 
        "ar1": ar1, 
        "ar2": ar2, 
        "ar3": ar3, 
        "ar4": ar4, 
        "ar5": ar5, 
        "ar6": ar6, 
        "pointer": pointer, 
        "foot": foot, 
        "foot2": foot2, 
        "hoof": hoof, 
        "hoof2": hoof2, 
        "sqr": sqr, 
        "cross": cross, 
        "hat": hat, 
        "head": head, 
        "scapula": scapula, 
    }
    inputs = {}
    for tmp in args:
        for key, val in tmp.items():
            if isinstance(val, dict):
                print("Dict in dict.")
            else:
                inputs[key] = val
    for key, val in kwargs.items():
        inputs[key] = val
    # If there is no inputs...
    if not inputs:
        tmp = input()
        coordinate = []
        try:
            for i in tmp.split(","):
                key, val = i.strip().split("=")
                if val == "True":
                    coordinate.append(ctrl[key])
                else:
                    continue
        except:
            print("Syntax is incorrect.")
    else:
        coordinate = [ctrl[i] for i in inputs if inputs[i]]
    result = [pm.curve(d=1, p=i) for i in coordinate]
    return result


def createJson(original_func):
    """ A decorator for creating Json files. """
    def wrapper(*args, **kwargs):
        fullPath = pm.Env().sceneName()
        if not fullPath:
            print("File not saved.")
        else:
            dir = os.path.dirname(fullPath)
            name_Ext = os.path.basename(fullPath)
            name, ext = os.path.splitext(name_Ext)
            jsonAll = [i for i in os.listdir(dir) if i.endswith('.json')]
            verDict = {}
            for i in jsonAll:
                tmp = re.search('(.*)[_v]([0-9]{4})[.].*', i)
                num = int(tmp.group(2))
                verDict[num] = tmp.group(1)
            if not verDict:
                jsonFile = dir + "/" + name + ".json"
                data = {}
            else:
                verMax = max(verDict.keys())
                jsonFile = f"{dir}/{verDict[verMax]}v%04d.json" % verMax
                with open(jsonFile) as JSON:
                    data = json.load(JSON)
            result = original_func(data, *args, **kwargs)
            with open(dir + "/" + name + ".json", 'w') as JSON:
                json.dump(data, JSON, indent=4)
            return result
    return wrapper


@createJson
def writeJSON(data: dict) -> None:
    sel = pm.ls(sl=True)
    if not sel:
        print("Nothing selected.")
    else:
        for j, k in enumerate(sel):
            if j % 2:
                continue
            else:
                obj = sel[j+1].name()
                cc = k.name()
                pm.parentConstraint(cc, obj, mo=True, w=1)
                # pm.scaleConstraint(cc, obj, mo=True, w=1)
                data[obj] = cc


@createJson
def loadJSON(data: dict) -> None:
    for obj, cc in data.items():
        pm.parentConstraint(cc, obj, mo=True, w=1)
        pm.scaleConstraint(cc, obj, mo=True, w=1)


def grouping(*args):
    """ Grouping itself and named own """
    sel = args if args else pm.ls(sl=True)
    for i in sel:
        grp = pm.group(i, n="%s_grp" % i)
        pm.xform(grp, os=True, piv=(0,0,0))


def groupingNull(*args):
    """ Grouping null """
    sel = args if args else pm.ls(sl=True)
    for i in sel:
        grp = pm.group(i, n=f"{i}_null", r=True, )
        pm.xform(grp, os=True, piv=(0,0,0))


def groupingEmpty(*args: str) -> list:
    """ Create an empty group and match the pivot with the selector. """
    sel = args if args else pm.ls(sl=True)
    grpName = []
    for i in sel:
        grp = pm.group(em=True, n = i + "_grp")
        grpName.append(grp)
        pm.matchTransform(grp, i, pos=True, rot=True)
        try:
            mom = i.getParent()
            pm.parent(grp, mom)
        except:
            pass
        pm.parent(i, grp)
    return grpName


def deletePlugins():
    """ Attempt to delete unused plugins. """
    unknownList = pm.ls(type="unknown")
    # Just delete Unknown type list.
    pm.delete(unknownList)
    pluginList = pm.unknownPlugin(q=True, l=True)
    if not pluginList:
        print("There are no unknown plugins.")
    else:
        for j, k in enumerate(pluginList):
            pm.unknownPlugin(k, r=True)
            # Print deleted plugin's names and number
            print(f"{j} : {k}")
        print('Delete completed.')


def selectObj():
    """ Select mesh only. """
    sel = pm.ls(sl=True, dag=True, type=['mesh', 'nurbsSurface'])
    obj = {i.getParent() for i in sel}
    result = list(obj)
    pm.select(result)


def selectGrp():
    """ If there is no shape and the object type is not 
    'joint', 'ikEffector', 'ikHandle', and 'Constraint', 
    then it is most likely a group. """
    sel = pm.ls(sl=True, dag=True, type=['transform'])
    grp = []
    for i in sel:
        typ = pm.objectType(i)
        A = pm.listRelatives(i, s=True)
        B = typ in ['joint', 'ikEffector', 'ikHandle',]
        C = 'Constraint' in typ
        if not (A or B or C):
            grp.append(i)
        else:
            continue
    pm.select(grp)


def selectConst():
    """ If there is no shape and the object type is not 
    'joint', 'ikEffector', 'ikHandle', and not 'Constraint', 
    then it is most likely a Constraints. """
    sel = pm.ls(sl=True, dag=True, type=['transform'])
    grp = []
    for i in sel:
        typ = pm.objectType(i)
        A = pm.listRelatives(i, s=True)
        B = typ in ['joint', 'ikEffector', 'ikHandle',]
        C = 'Constraint' in typ
        if not (A or B or not C):
            grp.append(i)
        else:
            continue
    pm.select(grp)


def selectJnt():
    """ Select only joints. """
    sel = pm.ls(sl=True, dag=True, type=['transform'])
    grp = []
    for i in sel:
        typ = pm.objectType(i)
        if typ != 'joint':
            continue
        else:
            grp.append(i)
    pm.select(grp)


def selectVerts_influenced():
    """ Select the bone first, and the mesh at the end. """
    sel = pm.ls(sl=True)
    num = len(sel)
    if num != 2:
        return
    bone = sel[0]
    mesh = sel[-1]
    if pm.objectType(bone) != 'joint':
        print("Select the bone first.")
    elif not mesh.getShape():
        print("the mesh at the end.")
    else:
        skin = mesh.listHistory(type="skinCluster")
        pm.skinCluster(skin, e=True, siv=bone)


def check_sameName():
    """ Select objects with duplicate names. """
    sel = pm.ls(tr=True) # tr: transform object
    dup = [i for i in sel if "|" in i]
    if not dup:
        print("No duplicated names.")
    else:
        pm.select(dup)


def zeroPivot():
    """ Move pivot to zero. """
    sel = pm.ls(sl=True)
    for i in sel:
        j = f"{i}.scalePivot"
        k = f"{i}.rotatePivot"
        pm.move(0, 0, 0, j, k, rpr=True)


def rename(*arg: str) -> None:
    """ Rename by incrementing the last digit in the string. """
    lenArg = len(arg)
    sel = pm.ls(sl=True)
    # Given a single argument, create a new name.
    if not sel or lenArg == 0:
        return
    elif lenArg == 1:
        txt = arg[0]
        # txtList -> ['testName', '23', '_', '17', '_grp']
        txtList = re.split(r'([^0-9]+)([0-9]*)', txt)
        txtList = [i for i in txtList if i]
        # txtDict -> {1: (23, 2), 3: (17, 2)}
        txtDict = {}
        for i, n in enumerate(txtList):
            if n.isdigit():
                txtDict[i] = (int(n), len(n))
            else:
                continue
        if len(txtDict):
            idx = max(txtDict) # idx -> 3
            numTuple = txtDict[idx] # numTuple -> (17, 2)
            num = numTuple[0] # num -> 17
            numDigit = numTuple[1] # numDigit -> 2
            for j, k in enumerate(sel):
                numStr = str(num + j) # increase by j
                numLen = len(numStr) # digit of numStr
                # Match <numStr> with the input <numDigit>
                if numLen < numDigit:
                    sub = numDigit - numLen
                    numStr = '0'*sub + numStr
                txtList[idx] = numStr
                new = ''.join(txtList) # new -> 'testName23_17_grp'
                pm.rename(k, new)
        else:
            for j, k in enumerate(sel):
                new = ''.join(txtList) + str(j)
                pm.rename(k, new)
    # Two arguments replace words.
    elif lenArg == 2:
        before = arg[0]
        after = arg[1]
        for obj in sel:
            new = obj.replace(before, after)
            pm.rename(obj, new)
    else:
        return


def poleVector():
    """ Get the poleVector's position from 3 joints. """
    sel = pm.ls(sl=True) # Select three objects.
    if len(sel) != 3:
        print('Select three joints.')
    else:
        midJnt = sel[1]
        endJnt = sel[2]
        points = [pm.xform(i, q=True, ws=True, rp=True) for i in sel]
        p1, p2, p3 = [i for i in points]
        pm.select(cl=True)
        tmp1 = pm.joint(p=p1)
        tmp2 = pm.joint(p=p3)
        pm.joint(tmp1, e=True, oj='xyz', sao='yup', ch=True, zso=True)
        pm.joint(tmp2, e=True, oj='none', ch=True, zso=True)
        # o: offset, wut: worldUpType, wuo: worldUpObject
        pm.aimConstraint(endJnt, tmp1, o=(0,0,90), wut='object', wuo=midJnt)
        # cn: constraint
        pm.delete(tmp1, cn=True)
        pm.matchTransform(tmp1, midJnt, pos=True)
        loc = pm.spaceLocator()
        pm.matchTransform(loc, tmp2, pos=True, rot=True)
        # Delete temporarily used joints.
        pm.delete(tmp1)


def openFolder():
    """ Open the Windows folder 
    and copy the fullPath to the clipboard.
     """
    fullPath = pm.Env().sceneName()
    dir = os.path.dirname(fullPath)
    # copy the fullPath to the clipboard.
    # subprocess.run("clip", text=True, input=fullPath)
    os.startfile(dir)


def lineStraight():
    """ Arrange the points in a straight line.
    Use the equation of a straight line in space 
    to make a curved line a straight line.
    1. Create an equation
    2. Check the condition.
    3. Make a straight line.
     """
    sel = pm.ls(sl=True, fl=True)
    if not sel:
        print('Nothing selected.')
        return
    alpha = sel[0]
    omega = sel[-1]
    # Copy the original backUp
    tmp = pm.ls(sel, o=True)
    dup = pm.duplicate(tmp, rr=True)
    dup = dup[0]
    # makeEquation
    X1, Y1, Z1 = alpha.getPosition(space="world")
    X2, Y2, Z2 = omega.getPosition(space="world")
    A, B, C = (X2 - X1), (Y2 - Y1), (Z2 - Z1)
    MAX = max([abs(i) for i in [A, B, C]])
    x, y, z = sympy.symbols('x y z')
    expr1 = sympy.Eq(B*x - A*y, B*X1 - A*Y1)
    expr2 = sympy.Eq(C*y - B*z, C*Y1 - B*Z1)
    expr3 = sympy.Eq(A*z - C*x, A*Z1 - C*X1)
    # Conditions
    if abs(A) == MAX:
        idx = 0
        xyz = x
        variables = [y, z]
        expr = [expr1, expr3]
    elif abs(B) == MAX:
        idx = 1
        xyz = y
        variables = [x, z]
        expr = [expr1, expr2]
    elif abs(C) == MAX:
        idx = 2
        xyz = z
        variables = [x, y]
        expr = [expr2, expr3]
    else:
        pass
    # makeStraight
    for i in sel:
        point = i.getPosition(space="world")
        value = point[idx]
        fx = [i.subs(xyz, value) for i in expr]
        sol = sympy.solve(fx, variables)
        sol[xyz] = value
        p1, p2, p3 = [round(float(sol[var]), 4) for var in [x, y, z]]
        pm.move(p1, p2, p3, i)


def lineStraight_rebuild():
    """ This way does not create an equation, 
    but uses rebuild to create a straight line. """
    sel = pm.ls(sl=True, fl=True)
    spans = len(sel) - 1
    alpha = sel[0].getPosition(space="world")
    omega = sel[-1].getPosition(space="world")
    cuv = pm.curve(d=1, p=[alpha, omega])
    pm.rebuildCurve(cuv, d=1, 
        ch=False, # constructionHistory
        s=spans, # spans
        rpo=True, # replaceOriginal
        end=1, # endKnots
        kr=0, # keepRange
        kt=0, # keepTangents
        )


def orientJnt(arg=None):
    """ Freeze and Orient joints
    Select only "joint", freeze and orient. 
    And the end joints inherit the orient of the parent joint.
     """
    if arg == None:
        sel = pm.ls(sl=True)
    elif isinstance(arg, str):
        sel = [arg]
    elif isinstance(arg, list):
        sel = arg
    else:
        return 0
    for jnt in sel:
        pm.select(jnt, hi=True)
        allSel = pm.ls(sl=True)
        isJnt = pm.objectType(jnt) == 'joint'
        allJnt = [i for i in allSel if isJnt]
        endJnt = [i for i in allJnt if not i.getChildren()]
        pm.select(cl=True)
        pm.makeIdentity(allJnt, a=True, jo=True, n=0)
        pm.joint(jnt, e=True, oj='yzx', sao='zup', ch=True, zso=True)
        for i in endJnt:
            pm.joint(i, e=True, oj='none', ch=True, zso=True)
    return sel


def jntNone(*arg: int) -> None:
    '''Change the drawing style of a joint.
    0: Bone
    1: Multi Child as Box
    2: None
    '''
    num = 2 if not arg else arg[0]
    sel = pm.ls(sl=True)
    if num < 0 or num > 2:
        msg = "Allowed numbers are "
        msg += "[0: Bone, 1: Multi Child as Box, 2: None]"
        print(msg)
    elif not sel:
        print("Nothing selected.")
    else:
        jnt = [i for i in sel if pm.objectType(i)=='joint']
        for i in jnt:
            pm.setAttr(f"{i}.drawStyle", num)


def attr_geoHide():
    """ Create and connect <Geo_Hide> channels
    1. Select a few geo group.
    2. The Last one should be the Controller. 
     """
    sel = pm.ls(sl=True)
    ctrl = sel.pop()
    attr = "Geo"
    vis = "visibility"
    pm.addAttr(ctrl, ln=attr, at='bool')
    pm.setAttr(f'{ctrl}.{attr}', e=True, k=True)
    for geo in sel:
        pm.connectAttr(f"{ctrl}.{attr}", f"{geo}.{vis}", f=True)


def attr_subCtrl():
    """ Create and connect <Sub_Ctrl> channels
    1. Select a few <sub ctrl> group.
    2. The Last one should be the Controller. 
     """
    sel = pm.ls(sl=True)
    ctrl = sel.pop()
    attr = "Sub_Ctrl"
    vis = "visibility"
    pm.addAttr(ctrl, ln=attr, at='bool')
    pm.setAttr(f'{ctrl}.{attr}', e=True, k=True)
    for grp in sel:
        pm.connectAttr(f"{ctrl}.{attr}", f"{grp}.{vis}", f=True)


def getPointPosition():
    """ Returns the coordinates of points as a list. """
    sel = pm.ls(sl=True, fl=True)
    result = []
    for i in sel:
        x, y, z = pm.pointPosition(i)
        x = round(x, 3)
        y = round(y, 3)
        z = round(z, 3)
        result.append((x, y, z))
    print(result)
    return result


# Offset the Keys
def keyOff(i=1): # i : interval
    sel = pm.ls(sl=True, fl=True)
    for j, k in enumerate(sel):
        pm.keyframe(k, e=True, r=True, tc = j * i)


# Create strokes and convert them to polygons
def createStroke(cuv):
    pm.select(cl=True)
    pm.select(cuv)
    mel.eval("AttachBrushToCurves;")
    strok = pm.ls(sl=True, dag=True, s=True)
    strok = strok[0]
    brush = [i for i in strok.inputs() if pm.nodeType(i)=="brush"]
    brush = brush[0]
    pm.setAttr(f'{brush}.globalScale', 30)
    mel.eval("doPaintEffectsToPoly(1, 0, 1, 1, 100000);")
    pTube = [i.getParent() for i in pm.ls(sl=True)]
    pTube = pTube[0]
    pTubeGrp = pTube.getParent()
    newName = cuv.replace('cuv_', 'newObj_')
    pm.parent(pTube, w=True)
    pm.rename(pTube, newName)
    pm.delete(pTubeGrp)


def makeFolder():
    """ Copy Source folder to New Folder """
    src = r"T:\AssetTeam\Share\Templates\MayaProjectSample"
    folder = pm.fileDialog2(fm=0, ds=2, okc='Create', cap='Create Folder')
    srcCheck = os.path.isdir(src)
    if not srcCheck:
        print("There is no source folder.\n", src)
        return
    elif folder == None:
        return
    else:
        folder = folder[0]
        folderPath = os.path.splitext(folder)[0]
        shutil.copytree(src, folderPath)
        os.startfile(folderPath)
        return folderPath


def removeDeformed():
    """ Remove Deformed from all objects including the text Deformed.
     """
    OLD = "Deformed"
    NEW = ""
    nodes = pm.ls("*{}*".format(OLD), r=True)
    for node in nodes:
        new_name = node.name().replace(OLD, NEW)
        node.rename(new_name)


def getMaxVersion(fullPath: str) -> int:
    """ Given an address, it lists the Maya files in that folder. 
    And check if there is a version in the file name, 
    returns the largest number. 
        """
    folder = pathlib.Path(fullPath)
    if folder.is_file():
        folder = folder.parent
    pattern1 = re.compile(".*v(\d{4})") # v0001 ~ v9999
    number = []
    for i in folder.glob("*.ma"):
        ver = pattern1.match(i.name)
        if not ver:
            continue
        num = ver.group(1)
        num = int(num)
        if num == 9999:
            continue
        else:
            number.append(num)
    try:
        result = max(number)
    except:
        result = 0
    return result


def copyHJK():
    """ Copy hjk.py 
    from <in git folder> to <maya folder in MyDocuments> """
    scriptsFolder = pm.internalVar(usd=True)
    tmp = scriptsFolder.rsplit("/", 5)[0]
    gitFolder = tmp + "/Desktop/git/maya/hjk.py"
    docFolder = scriptsFolder + "hjk.py"
    print(f"{gitFolder} -> {docFolder}")
    shutil.copy(gitFolder, docFolder)


def parentParty(n: int):
    """ It is used when you want to make the selected joints 
    into n hierarchical structures. n is the bundle unit.
    Example: When n is 4, 
    joints can be created in the following hierarchical structure.
    joint0
        joint1
            joint2
                joint3
     """
    sel = pm.ls(sl=True)
    for j, k in enumerate(sel):
        mod = j % n
        if mod == 0:
            continue
        else:
            pm.parent(k, sel[j-1])


# 79 char line ================================================================
# 72 docstring or comments line ========================================


# createLoc()
# AutoRig_Wheel()
# AutoWheel_Rig2()
# groupingEmpty()
# rename("_L_", "_R_")
# ctrl(cir=True)
# Colors()
# check_sameName()
# attr_geoHide()
# poleVector()
# orientJnt()
# parentParty(4)
# removeDeformed()
# SoftSel()
# zeroPivot()