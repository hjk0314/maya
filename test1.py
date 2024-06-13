from general import *
import pymel.core as pm


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
                name = self.swapLeftAndRight(obj)
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
    def swapLeftAndRight(self, objName):
        if '_L' in objName:
            result = objName.replace('_L', '_R')
        elif '_R' in objName:
            result = objName.replace('_R', '_L')
        elif 'Left' in objName:
            result = objName.replace('Left', 'Right')
        elif 'Right' in objName:
            result = objName.replace('Right', 'Left')
        else:
            result = ''
        return result


    # Create a mirrored group.
    def mirrorGroup(self, selection):
        name = self.swapLeftAndRight(selection.name())
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

