import re
import itertools
import pymel.core as pm


def channelList():
    TRS = ['t', 'r', 's']
    XYZ = ['x', 'y', 'z']
    PRO = itertools.product(TRS, XYZ)
    # PRO: [('t', 'x'), ('t', 'y'), ... ('s', 'z')]
    channel = [''.join(i) for i in PRO]
    channel += ['v']
    # ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
    return channel


def selConst():
    sel = pm.ls(sl=True, dag=True)
    STR = re.compile(r'.+Constraint[0-9]?')
    constList = []
    for i in sel:
        typ = pm.objectType(i)
        if STR.search(typ):
            constList.append(i)
        else:
            continue
    # pm.select(constList)
    return constList


def selJnt():
    sel = pm.ls(sl=True, dag=True)
    jnt = []
    for i in sel:
        typ = pm.objectType(i, i='joint')
        if typ:
            jnt.append(i)
        else:
            continue
    # pm.select(jnt)
    return jnt


def main():
    const = selConst()
    jnt = selJnt()
    channel = channelList()
    pm.delete(const)
    for i in jnt:
        pm.delete(i, cn=True)
        for j in channel:
            pm.disconnectAttr(i + j)


main()