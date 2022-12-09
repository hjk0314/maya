import pymel.core as pm
import hjk


winName = 'test'
if pm.window(winName, exists=True):
    pm.deleteUI(winName)
else:
    win = pm.window(winName, t='temp', s=True, rtf=True)
    pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=278)
    pm.separator(h=10)
    pm.rowColumnLayout(nc=3, cw=[(1, 90), (2, 90), (3, 90)])
    pm.button(l='Han', c=lambda x: hjk.Han())
    pm.button(l='AutoWheel', c=lambda x: hjk.AutoWheel())
    pm.button(l='MatchPivot', c=lambda x: hjk.MatchPivot())
    pm.button(l='MirrorCopy', c=lambda x: hjk.MirrorCopy())
    pm.button(l='ThroughCurve', c=lambda x: hjk.ThroughCurve())
    pm.button(l='MatchCuvShape', c=lambda x: hjk.MatchCuvShape())
    pm.button(l='Human', c=lambda x: hjk.Human())
    pm.button(l='LineBridge', c=lambda x: hjk.LineBridge())
    pm.button(l='cuvLoc', c=lambda x: hjk.cuvLoc())
    pm.button(l='delPlugin', c=lambda x: hjk.delPlugin())
    pm.button(l='grp', c=lambda x: hjk.grp())
    pm.button(l='grpEmpty', c=lambda x: hjk.grpEmpty())
    pm.button(l='selGrp', c=lambda x: hjk.selGrp())
    pm.button(l='sameName', c=lambda x: hjk.sameName())
    pm.button(l='zeroPivot', c=lambda x: hjk.zeroPivot())
    pm.button(l='poleVector', c=lambda x: hjk.poleVector())
    pm.button(l='openSaved', c=lambda x: hjk.openSaved())
    pm.button(l='createLoc', c=lambda x: hjk.createLoc())
    pm.button(l='createLine', c=lambda x: hjk.createLine())
    pm.button(l='makeStraight', c=lambda x: hjk.makeStraight())
    pm.button(l='makeStraight2', c=lambda x: hjk.makeStraight2())
    pm.button(l='pathAni', c=lambda x: hjk.pathAni())
    pm.button(l='writeJSON', c=lambda x: hjk.writeJSON())
    pm.button(l='loadJSON', c=lambda x: hjk.loadJSON())
    pm.button(l='orientJnt', c=lambda x: hjk.orientJnt())
    pm.button(l='jntNone', c=lambda x: hjk.jntNone(2))
    pm.button(l='jntBone', c=lambda x: hjk.jntNone(0))
    pm.button(l='hjkCopy', c=lambda x: hjk.hjkCopy())
    pm.setParent("..", u=True)
    pm.separator(h=10)
    pm.showWindow(win)



