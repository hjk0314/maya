import pymel.core as pm

def find_mirror_vertices(*args, tolerance=0.001):
    """
    주어진 X>0 버텍스들에 대응하는 X<0 버텍스를 찾되,
    미러 위치와의 거리가 tolerance를 넘으면 무시합니다.

    Args:
        *args: 버텍스 이름(str) 혹은 MeshVertex(PyNode)들.
        tolerance (float): 미러 위치까지의 최대 허용 오차 (world 단위).
    
    Returns:
        dict: {원본버텍스: 대응버텍스 or None} 형태의 딕셔너리.
    """
    # 입력을 MeshVertex 객체로 통일
    verts = []
    for v in args:
        node = pm.PyNode(v)
        if isinstance(node, pm.MeshVertex):
            verts.append(node)
        else:
            pm.warning(f"{v}는 MeshVertex가 아닙니다. 무시합니다.")
    if not verts:
        pm.warning("처리할 버텍스가 없습니다.")
        return {}

    mesh = verts[0].node()
    all_verts = mesh.vtx
    positions = [vtx.getPosition(space="world") for vtx in all_verts]

    results = {}
    tol2 = tolerance ** 2

    for src in verts:
        pos = src.getPosition(space="world")
        # X>0 만 처리
        if pos.x <= 0:
            results[src] = None
            continue

        mirror_pos = pm.datatypes.Point(-pos.x, pos.y, pos.z)

        # 최소 거리 계산
        min_idx, min_dist = None, float("inf")
        for i, pt in enumerate(positions):
            dx = pt.x - mirror_pos.x
            dy = pt.y - mirror_pos.y
            dz = pt.z - mirror_pos.z
            dist2 = dx*dx + dy*dy + dz*dz
            if dist2 < min_dist:
                min_idx, min_dist = i, dist2

        # 허용 오차 넘으면 무시
        if min_dist > tol2:
            results[src] = None
        else:
            results[src] = all_verts[min_idx]

    return results
