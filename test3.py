import pymel.core as pm


def get_deformed_shape(obj):
    node = pm.PyNode(obj)
    shapes = node.getShapes() if isinstance(node, pm.nt.Transform) else [node]
    if not shapes:
        raise RuntimeError(f"No shape found on '{obj}'")
    def is_deformed_mesh(s):
        return (
            isinstance(s, pm.nt.Mesh)
            and not s.intermediateObject.get()
            and not s.isReferenced()
        )
    for s in shapes:
        if is_deformed_mesh(s):
            return s.name().split('|')[-1].split(':')[-1]
    for s in shapes:
        if isinstance(s, pm.nt.Mesh) and not s.intermediateObject.get():
            return s.name().split('|')[-1].split(':')[-1]
    s = shapes[0]
    return s.name().split('|')[-1].split(':')[-1]


print(get_deformed_shape("char_tigerA_mdl_v9999:tigerA_body"))

