import pymel.core as pm
from pymel.core.datatypes import Vector


def assignSkinWeightsByDistance():
    sel = pm.ls(selection=True, flatten=True)
    joints = [x for x in sel if isinstance(x, pm.nodetypes.Joint)]
    verts  = [x for x in sel if isinstance(x, pm.MeshVertex)]
    
    if not verts:
        pm.error("Skin Weight: ")
    if not joints:
        pm.error("Skin Weight: ")
    
    for vtx in verts:
        meshShape = vtx.node()
        skins = [n for n in pm.listHistory(meshShape) if isinstance(n, pm.nt.SkinCluster)]
        if not skins:
            pm.warning(f"{meshShape}")
            continue
        skin = skins[0]
        

        allInfls = pm.skinCluster(skin, query=True, influence=True)
        pm.skinPercent(skin, vtx, transformValue=[(inf, 0.0) for inf in allInfls])
        

        vPos = Vector(vtx.getPosition(space='world'))
        distances = []
        for j in joints:
            jPos = Vector(j.getTranslation(space='world'))
            distances.append((vPos - jPos).length())
        

        if any(d == 0 for d in distances):
            weights = [1.0 if d == 0 else 0.0 for d in distances]
        else:
            invs = [1.0 / d for d in distances]
            total = sum(invs)
            weights = [inv / total for inv in invs]
        

        pm.skinPercent(skin, vtx, transformValue=list(zip(joints, weights)))
        
        
        msg = ", ".join(f"{j.name()}={w:.3f}" for j, w in zip(joints, weights))
        print(f"[assignSkinWeightsByDistance] {vtx} {msg}")



