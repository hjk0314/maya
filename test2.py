import maya.standalone
maya.standalone.initialize(name='python')
import pymel.core as pm


old_string = "Deformed"
new_string = ""


pm.openFile(r"C:\Users\jkhong\Desktop\a_rig.ma")

pm.saveFile()

nodes = pm.ls("*{}*".format(old_string), recursive=True)


for node in nodes:
    new_name = node.name().replace(old_string, new_string)
    node.rename(new_name)


pm.saveFile()


pm.shutdown()
maya.standalone.uninitialize()
