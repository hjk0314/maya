import pymel.core as pm


class MirrorCopy:
    def __init__(self, idx: str):
        '''Copy the group and mirror it in the direction. 
        If there is a curve in it, copy the curve and mirror it.
        '''
        self.idx = idx
        self.sel = pm.ls(sl=True)
        self.main()


    # Check the conditions.
    def main(self):
        if self.idx != 'x' and self.idx != 'z':
            print("X and Z directions are available.")
        elif not self.sel:
            print("Nothing selected.")
        else:
            for i in self.sel:
                self.mirrorCopy(i)


    # If there is a curve in the group, copy the curve and mirror it.
    def mirrorCopy(self, selection):
        cuv = selection.getChildren()
        shp = pm.ls(cuv, dag=True, s=True)
        typ = 'nurbsCurve'
        objList = {i.getParent().name() for i in shp if pm.objectType(i)==typ}
        objList = list(objList)
        if not objList:
            self.mirrorGroup(selection)
        else:
            for obj in objList:
                name = self.swapLR(obj)
                copy = pm.duplicate(obj, rr=True, n=name)
                pm.parent(copy, w=True)
                grp = pm.group(em=True)
                pm.parent(copy, grp)
                direction = [-1, 1, 1] if self.idx == 'x' else [1, 1, -1]
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
        if self.idx == 'x':
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



def createCC(ratio: int = 0.5):
    sel = pm.ls(sl=True)
    if not sel:
        print("Noting selected.")
    else:
        for j, k in enumerate(sel):
            name = k.replace('jnt', 'cc')
            cuv = pm.circle(nr=(1,0,0), ch=True, n=name)
            pm.matchTransform(cuv, k, pos=True, rot=True)
            decrease = 1 - (ratio*j/len(sel))
            pm.scale(cuv, [decrease, decrease, decrease], r=True)


def parentCC(num: int, name: str):
    nameA = name
    if '_L' in nameA:
        nameB = name.replace('_L', '_R')
    elif '_R' in nameA:
        nameB = name.replace('_R', '_L')
    else:
        nameB = ''
    if not nameB:
        for i in range(1, num):
            cc = nameA + '%d' % i
            grp = nameA + '%d_grp' % (i+1)
            pm.parent(grp, cc)
    else:
        for i in range(1, num):
            cc = nameA + '%d' % i
            grp = nameA + '%d_grp' % (i+1)
            pm.parent(grp, cc)
            cc = nameB + '%d' % i
            grp = nameB + '%d_grp' % (i+1)
            pm.parent(grp, cc)


# parentCC(5, 'cc_spine_')
# createCC(0.75)