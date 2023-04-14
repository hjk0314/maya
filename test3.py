import sys
import maya.standalone
maya.standalone.initialize(name='python')
import pymel.core as pm


if len(sys.argv) >1:
    tmp = sys.argv[1]
# pm.newFile(force=True)
pm.openFile(r"C:\Users\hjk03\Desktop\test.ma", f=True)
selection = pm.ls()
poly_selection = []
for obj in selection:
    if obj.type() == 'transform':
        shape_node = obj.getShape()
        if shape_node and shape_node.nodeType() == 'mesh':
            poly_selection.append(obj)
for num, poly in enumerate(poly_selection):
    result = pm.rename(poly.name(), f"{tmp}_{num}")
    print(result)
pm.saveFile(f=True)
# for i in range(4):
#     pm.polySphere()
# pm.saveAs(r"C:\Users\hjk03\Desktop\test.ma")
maya.standalone.uninitialize()