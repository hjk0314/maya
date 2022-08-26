import maya.cmds as cmds
import maya.mel as mel
import check
import tools


cmds.evalDeferred('createMenuBar()')
def createMenuBar():
    # UI start ==========================================================================
    # gMW = pm.language.melGlobals["gMainWindow"]
    gMW = mel.eval("$tmpVar=$gMainWindow")
    menu_id = "hjk0314"
    menu_lbl = "홍진기"
    if cmds.menu(menu_id, l=menu_lbl, exists=True, p=gMW):
        cmds.deleteUI(cmds.menu(menu_id, e=True, dai=True))
    mainMenu = cmds.menu(menu_id, l=menu_lbl, p=gMW, to=True)
    # UI end ============================================================================
    #
    # menu start ========================================================================
    # Check
    cmds.menuItem(l="검사", subMenu=True, p=mainMenu, to=True) # to: tearOff
    cmds.menuItem(l="중복 이름 검사", c=lambda x: check.sameName())
    cmds.setParent("..", menu=True)
    # Tools
    cmds.menuItem(l="도구", subMenu=True, p=mainMenu, to=True)
    cmds.menuItem(l="쉐이더 투 제이슨", c=lambda x: tools.abc())
    cmds.menuItem(l="감염 치료", c=lambda x: tools.vaccine())
    cmds.menuItem(l="언노운 플러그인 제거", c=lambda x: tools.delPlugin())
    cmds.setParent("..", menu=True)
    # menu end ==========================================================================

