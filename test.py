import pymel.core as pm


def scaleUp_wheelCtrl(obj, ctrl, sizeUp):
    """ Create the controller 1.2 times the size of the object.
    The pmNode variable checks 
    whether the input obj is a string or a pymel class, 
    in order to use BoundingBox() method. """
    pmNode = pm.nodetypes.Transform
    obj = obj if isinstance(obj, pmNode) else pm.ls(obj)[0]
    bb = obj.getBoundingBox()
    diameter = bb.max() - bb.min()
    scl = [round(i*0.5*sizeUp, 3) for i in diameter]
    pm.scale(ctrl, scl)





