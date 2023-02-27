import pymel.core as pm


class SolariBoard:
    def __init__(self):
        """ A Class to create a solariBoard. 
        Select the cards in order and call the class. 
        Enter the name of the controller in the "input() window". 
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


