import maya.standalone
import maya.cmds as cmds


def standalone_template():
    # Start in batch mode
    maya.standalone.initialize(name='python')
    cmds.file("C:/Users/hjk03/Desktop/a.ma", f=True, o=True)
    print(cmds.ls(dag=True, s=True))
    # Do your magic here
    # Save it
    # cmds.file(s=True, f=True)

