import maya.cmds as cmds


# Create channel
cmds.attributeQuery('FKIK', node='controller', ex=True)
cmds.addAttr('controller', ln='visibility', at='float', dv=0)
cmds.setAttr('controller.visibility', e=True, k=True)


# s: string, o: object, ae: alwaysEvaluate, uc: unitConversion
cmds.expression(s='''src''', o='', ae=1, uc='all')


# delete and disconnect.
cmds.nodeType('obj') # Result: transform
cmds.disconnectAttr('obj.tx')
cmds.delete('obj', cn=True) # cn: constraints


# shape, object, shadingEngine, material
shp = cmds.ls(sl=True, dag=True, s=True)[0]
obj = cmds.listRelatives(shp, p=True)[0]
shd = cmds.listConnections(shp, type='shadingEngine')[0]
mat = cmds.ls(cmds.listConnections(shd), mat=True)[0]


# 79 char line ================================================================
# 72 docstring or comments line ========================================


