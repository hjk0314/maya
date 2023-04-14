import pymel.core as pm


def removeDeformed():
    OLD = "Deformed"
    NEW = ""
    nodes = pm.ls("*{}*".format(OLD), r=True)
    for node in nodes:
        new_name = node.name().replace(OLD, NEW)
        node.rename(new_name)

removeDeformed()