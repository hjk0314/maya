import hjk
import pymel.core as pm


def createLocatorWhisker():
    sel = pm.selected(sl=True)
    result = []
    for i in sel:
        loc = pm.spaceLocator(p=(0, 0, 0), n=f"loc_{i}")
        pm.matchTransform(loc, i, pos=True)
        result.append(loc)
    return result


def create_follicleConstraint(mesh, ctrl):
    locators = createLocatorWhisker()
    for loc in locators:
        uvs = hjk.getLocatorUV_onMesh(loc, mesh)
        fol = hjk.createFollicles(mesh, uvs,)
        tmp = loc.split("_")
        grp = "_".join(tmp[1:]) + "_grp"
        pm.parentConstraint(fol, grp, mo=True, w=1.0)
        pm.scaleConstraint("cc_sub", grp, mo=True, w=1.0)
        pm.delete(loc)

        # null = "_".join(tmp[1:]) + "_null"
        # pm.connectAttr(f"{ctrl}.rotate", f"{null}.rotate", f=True)


# hjk.groupOwnPivot(null=True)
# hjk.mirrorCopy(ctrl)


mesh = "char_tigerA_mdl_v9999:tigerA_body"
ctrl = "cc_whisker_C"
create_follicleConstraint(mesh, ctrl)