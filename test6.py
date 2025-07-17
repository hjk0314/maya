import pymel.core as pm

def get_vertex_weights(*vertices):
    """
    주어진 버텍스 각각에 대해 영향을 주는 조인트와 가중치를 반환합니다.

    Args:
        *vertices (str or MeshVertex): 
            "pSphere1.vtx[11]" 같은 문자열 또는 MeshVertex(PyNode)를 
            여러 개 넘겨줄 수 있습니다.

    Returns:
        dict[str, dict[str, float]]: 
            {
                "pSphere1.vtx[11]": {"leftjoint": 0.3, "rightjoint": 0.3, "centerjoint": 0.4},
                "pSphere1.vtx[12]": { … }
            }
    """
    result = {}
    for v in vertices:
        try:
            mv = pm.PyNode(v)
        except RuntimeError:
            pm.warning(f"'{v}' 를 PyNode로 변환할 수 없습니다. 무시합니다.")
            continue

        if not isinstance(mv, pm.MeshVertex):
            pm.warning(f"{mv}는 MeshVertex가 아닙니다. 무시합니다.")
            continue

        mesh = mv.node()
        skins = pm.listHistory(mesh, type='skinCluster')
        if not skins:
            pm.warning(f"{mesh}에 연결된 skinCluster가 없습니다.")
            result[mv.name()] = {}
            continue

        sc = skins[0]
        weight_map = {}
        for inf in sc.getInfluence():
            w = sc.getWeight(vtx=mv, influence=inf)
            if w > 0.0:
                weight_map[inf.name()] = w

        result[mv.name()] = weight_map

    return result
