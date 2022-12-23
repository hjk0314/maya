import maya.cmds as cmds
import maya.OpenMaya as om


class MappingCameraKeyToImage():
    def __init__(self):
        self.setupUI()


    def setupUI(self):
        if cmds.window('MCKTI', exists=True):
            cmds.deleteUI('MCKTI')
        else:
            title = 'Move the cameras keys and map the image accordingly'
            win = cmds.window('MCKTI', t=title, s=True, rtf=True)
            cmds.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=300)
            cmds.separator(h=10)
            fieldLbl = 'Move to keyframe : '
            self.keyField = cmds.intFieldGrp(l=fieldLbl, nf=1, v1=0)
            buttonLbl = 'Move camera keys, mapping image.'
            cmds.button(l=buttonLbl, c=lambda x: self.mapCameraKeyImage())
            cmds.separator(h=10)
            cmds.showWindow(win)
    
    
    # Move the camera's keys and map the image accordingly.
    def mapCameraKeyImage(self):
        destinationKey = cmds.intFieldGrp(self.keyField, q=True, v1=True)
        sel = cmds.ls(sl=True, dag=True, type=['camera']) # ['cameraShape1']
        cam = cmds.listRelatives(sel, p=True) # ['camera1']
        try:
            currentKey = min(cmds.keyframe(cam, q=True))
            value = destinationKey - currentKey
        except:
            value = 0 # Nothing happens
            om.MGlobal.displayError("The camera has no keyframes.")
        img = cmds.listRelatives(sel, c=True) # ['imagePlane1']
        imgShape = cmds.listRelatives(img, c=True) # ['imagePlaneShape1']
        if img:
            cmds.keyframe(cam, e=True, r=True, tc=value)
            frameOffset = cmds.getAttr(imgShape[0] + ".frameOffset")
            cmds.setAttr(imgShape[0] + ".frameOffset", frameOffset - value)
        else:
            om.MGlobal.displayError("There is no imagePlane.")


# 79 char line ================================================================
# 72 docstring or comments line ========================================


