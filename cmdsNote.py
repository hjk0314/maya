import maya.cmds as cmds


# xform
cmds.xform('obj', q=True, t=True, ws=True)


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


# 79 char line ================================================================
# 72 docstring or comments line ========================================

