import maya.cmds as cmds
import maya.mel as mel


cmds.evalDeferred('createMenuBar()')
def createMenuBar():
    # UI start ==========================================================================
    # gMW = pm.language.melGlobals["gMainWindow"]
    gMW = mel.eval("$tmpVar=$gMainWindow")
    menu_id = "hjk0314"
    menu_lbl = "mmp"
    if cmds.menu(menu_id, l=menu_lbl, exists=True, p=gMW):
        cmds.deleteUI(cmds.menu(menu_id, e=True, dai=True))
    mainMenu = cmds.menu(menu_id, l=menu_lbl, p=gMW, to=True)
    # UI end ============================================================================
    #
    # menu start ========================================================================
    # Check
    cmds.menuItem(l="Check", subMenu=True, p=mainMenu, to=True)
    cmds.menuItem(l="Same Names", c=lambda x: print("same name"))
    cmds.menuItem(l="Name Rules", c=lambda x: print("bad name"))
    cmds.setParent("..", menu=True)
    # Tools
    cmds.menuItem(l="Tools", subMenu=True, p=mainMenu, to=True)
    cmds.menuItem(l="Export Shader to Json", c=lambda x: print("json"))
    cmds.menuItem(l="Speed", c=lambda x: print("speed"))
    cmds.menuItem(l="Delete Vaccine", c=lambda x: print("delete vaccine"))
    cmds.menuItem(l="Bundangmain", c=lambda x: print("bundang"))
    cmds.menuItem(l="Unknown Plugins", c=lambda x: print("unknown plugins"))
    cmds.setParent("..", menu=True)
    # Update
    cmds.menuItem(l="Modeling Update", c=lambda x: print("model update"))
    cmds.setParent("..", menu=True)
    # menu end ==========================================================================

