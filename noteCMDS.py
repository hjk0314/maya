import os
import maya.cmds as cmds
import pymel.core as pm


# 채널에 attribute가 있는지 체크한다. -> bool
cmds.attributeQuery('FKIK', node='controller', ex=True)
# 채널에 attribute를 추가할 때 사용. 아래 setAttr과 같이 사용해야 함.
cmds.addAttr('controller', ln='visibility', at='float', dv=0)
cmds.setAttr('controller.visibility', e=True, k=True)


# 익스프레션을 넣을 때 사용하는 cmds 명령어.
# s: string, o: object, ae: alwaysEvaluate, uc: unitConversion
cmds.expression(s='''src''', o='', ae=1, uc='all')


cmds.nodeType('obj') # Result: transform
cmds.objectType('obj') == "mesh" # nodeType 보다 많이 쓰여진다.
cmds.disconnectAttr('obj.tx') # 연결을 끊을 때 사용.
cmds.delete('obj', cn=True) # cn: constraints


# shape, object, shadingEngine, material
shp = cmds.ls(sl=True, dag=True, s=True)[0] # 쉐입을 선택하고
obj = cmds.listRelatives(shp, p=True)[0]
shd = cmds.listConnections(shp, type='shadingEngine')[0] # 쉐이딩 엔진
mat = cmds.ls(cmds.listConnections(shd), mat=True)[0] # 메테리얼


# 레퍼런스에 대한 정보
src = "C:/Users/jkhong/Desktop/a.abc"
fileName = os.path.basename(src)
name, ext = os.path.splitext(fileName)
# '크리에이트 레퍼런스'하면 리졸브 네임을 얻을 수 있다.
resolvedName = pm.createReference(
    src, # full path
    gl=True, # groupLocator
    shd="shadingNetworks", # sharedNodes
    mnc=False, # mergeNamespacesOnClash
    ns=name # namespace
)


# '레퍼런스 쿼리'를 통해 '레퍼런스 네임'을 알 수 있다.
# '레퍼런스 네임'을 얻으면 레퍼런스와 관련된 대부분의 일을 할 수 있다.
refName = pm.referenceQuery(resolvedName, rfn=True) # reference name


# '레퍼런스 쿼리'의 '옵션'을 통해 '네임스페이스'를 알 수 있지만,
# 할 수 있는 것이 별로 없다.
refNS = pm.referenceQuery(resolvedName, ns=True) # namespace


# '레퍼런스 쿼리'의 '옵션'을 통해 '레퍼런스 여부'를 알 수 있다.
isNodeReferenced = pm.referenceQuery(src, inr=True) # bool


# 레퍼런스의 제거는 방법이 아래와 같다.
# 중요: 리졸브 네임 또는 레퍼런스 네임이 필요하다.
pm.FileReference(resolvedName).remove()
pm.FileReference(refName).remove()



