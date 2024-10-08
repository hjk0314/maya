import pymel.core as pm


class Pose:
    def __init__(self):
        self.passengerBone = {
            "Hips": (0.0, 0.0, 0.0), 
            "Spine": (-12.579, 0.0, 0.0), 
            "Spine1": (10.039, 0.0, 0.0), 
            "Spine2": (10.039, 0.0, 0.0), 
            "Neck": (-11.713, 0.0, 0.0), 
            "Head": (0.895, 0.0, 0.0), 
            "HeadTop_End": (0.0, 0.0, 0.0), 
            "LeftShoulder": (16.78, 0.0, 0.0), 
            "LeftArm": (48.581, -20.667, 21.15), 
            "LeftForeArm": (3.699, 10.523, 60.398), 
            "LeftHand": (8.492, 28.583, 20.246), 
            "LeftHandThumb1": (0.122, -11.737, 19.569), 
            "LeftHandThumb2": (4.758, -0.442, -20.957), 
            "LeftHandThumb3": (4.758, -0.442, -20.957), 
            "LeftHandThumb4": (0.0, 0.0, 0.0), 
            "LeftHandIndex1": (6.909, 0.0, 0.0), 
            "LeftHandIndex2": (6.909, 0.0, 0.0), 
            "LeftHandIndex3": (6.909, 0.0, 0.0), 
            "LeftHandIndex4": (0.0, 0.0, 0.0), 
            "LeftHandMiddle1": (-8.919, 0.0, 0.0), 
            "LeftHandMiddle2": (20.35, 0.0, 0.0), 
            "LeftHandMiddle3": (20.35, 0.0, 0.0), 
            "LeftHandMiddle4": (0.0, 0.0, 0.0), 
            "LeftHandRing1": (-8.36, 0.0, 0.0), 
            "LeftHandRing2": (22.255, 0.0, 0.0), 
            "LeftHandRing3": (22.255, 0.0, 0.0), 
            "LeftHandRing4": (0.0, 0.0, 0.0), 
            "LeftHandPinky1": (-9.745, 0.0, 0.0), 
            "LeftHandPinky2": (20.536, 0.0, 0.0), 
            "LeftHandPinky3": (20.536, 0.0, 0.0), 
            "LeftHandPinky4": (0.0, 0.0, 0.0), 
            "RightShoulder": (16.78, 0.0, 0.0), 
            "RightArm": (55.242, 18.387, -17.189), 
            "RightForeArm": (0.0, 0.0, -60.636), 
            "RightHand": (-5.057, -30.169, -6.891), 
            "RightHandThumb1": (4.554, 23.401, -5.462), 
            "RightHandThumb2": (0.0, 0.0, 4.535), 
            "RightHandThumb3": (0.0, 0.0, 11.355), 
            "RightHandThumb4": (0.0, 0.0, 0.0), 
            "RightHandIndex1": (0.941, -11.446, -7.835), 
            "RightHandIndex2": (21.945, 0.0, 0.0), 
            "RightHandIndex3": (21.945, 0.0, 0.0), 
            "RightHandIndex4": (0.0, 0.0, 0.0), 
            "RightHandMiddle1": (5.47, -3.754, -1.137), 
            "RightHandMiddle2": (14.86, 0.0, 0.0), 
            "RightHandMiddle3": (14.86, 0.0, 0.0), 
            "RightHandMiddle4": (0.0, 0.0, 0.0), 
            "RightHandRing1": (5.47, -3.754, -1.137), 
            "RightHandRing2": (14.86, 0.0, 0.0), 
            "RightHandRing3": (14.86, 0.0, 0.0), 
            "RightHandRing4": (0.0, 0.0, 0.0), 
            "RightHandPinky1": (-2.209, -3.873, -0.626), 
            "RightHandPinky2": (9.846, 0.0, 0.0), 
            "RightHandPinky3": (14.089, 0.0, 0.0), 
            "RightHandPinky4": (0.0, 0.0, 0.0), 
            "LeftUpLeg": (97.448, 0.0, 0.0), 
            "LeftLeg": (-19.007, 0.0, 0.0), 
            "LeftFoot": (0.0, 0.0, 0.0), 
            "LeftToeBase": (0.0, 0.0, 0.0), 
            "LeftToe_End": (0.0, 0.0, 0.0), 
            "RightUpLeg": (97.448, 0.0, 0.0), 
            "RightLeg": (-19.007, 0.0, 0.0), 
            "RightFoot": (0.0, 0.0, 0.0), 
            "RightToeBase": (0.0, 0.0, 0.0), 
            "RightToe_End": (0.0, 0.0, 0.0), 
            }
        self.driverBone = {
            "Hips": (0.0, 0.0, 0.0), 
            "Spine": (-0.008, 0.0, 0.0), 
            "Spine1": (3.747, 0.0, 0.0), 
            "Spine2": (0.0, 0.0, 0.0), 
            "Neck": (0.0, 0.0, 0.0), 
            "Head": (7.044, 0.0, 0.0), 
            "HeadTop_End": (0.0, 0.0, 0.0), 
            "LeftShoulder": (14.21, 0.0, 0.0), 
            "LeftArm": (59.395, -28.85, 21.495), 
            "LeftForeArm": (0.0, 0.0, 50.811), 
            "LeftHand": (0.0, -37.36, 0.0), 
            "LeftHandThumb1": (26.105, 14.967, 3.435), 
            "LeftHandThumb2": (0.0, 0.0, -29.416), 
            "LeftHandThumb3": (0.0, 0.0, -4.914), 
            "LeftHandThumb4": (0.0, 0.0, 0.0), 
            "LeftHandIndex1": (1.267, 0.037, -1.68), 
            "LeftHandIndex2": (34.841, 0.0, 0.0), 
            "LeftHandIndex3": (34.841, 0.0, 0.0), 
            "LeftHandIndex4": (0.0, 0.0, 0.0), 
            "LeftHandMiddle1": (-3.553, -0.0, 7.142), 
            "LeftHandMiddle2": (51.13, 0.0, 0.0), 
            "LeftHandMiddle3": (51.13, 0.0, 0.0), 
            "LeftHandMiddle4": (0.0, 0.0, 0.0), 
            "LeftHandRing1": (-4.856, -1.856, 12.946), 
            "LeftHandRing2": (49.212, 0.0, 0.0), 
            "LeftHandRing3": (49.212, 0.0, 0.0), 
            "LeftHandRing4": (0.0, 0.0, 0.0), 
            "LeftHandPinky1": (0.102, -2.39, 26.951), 
            "LeftHandPinky2": (38.718, 0.0, 0.0), 
            "LeftHandPinky3": (38.718, 0.0, 0.0), 
            "LeftHandPinky4": (0.0, 0.0, 0.0), 
            "RightShoulder": (14.21, 0.0, 0.0), 
            "RightArm": (61.26, 24.454, -14.554), 
            "RightForeArm": (0.0, 0.0, -61.2), 
            "RightHand": (5.409, -53.848, 12.789), 
            "RightHandThumb1": (0.0, 0.0, 0.0), 
            "RightHandThumb2": (21.646, 0.0, 33.398), 
            "RightHandThumb3": (0.0, 0.0, 33.398), 
            "RightHandThumb4": (0.0, 0.0, 0.0), 
            "RightHandIndex1": (22.829, -3.383, 7.981), 
            "RightHandIndex2": (23.065, 0.0, 0.0), 
            "RightHandIndex3": (23.065, 0.0, 0.0), 
            "RightHandIndex4": (0.0, 0.0, 0.0), 
            "RightHandMiddle1": (33.873, 0.0, 0.0), 
            "RightHandMiddle2": (33.873, 0.0, 0.0), 
            "RightHandMiddle3": (33.873, 0.0, 0.0), 
            "RightHandMiddle4": (0.0, 0.0, 0.0), 
            "RightHandRing1": (31.071, -0.666, -11.081), 
            "RightHandRing2": (30.626, -4.386, -0.998), 
            "RightHandRing3": (30.626, -4.386, -0.998), 
            "RightHandRing4": (0.0, 0.0, 0.0), 
            "RightHandPinky1": (29.968, 6.188, -26.792), 
            "RightHandPinky2": (32.073, 0.0, 0.0), 
            "RightHandPinky3": (32.073, 0.0, 0.0), 
            "RightHandPinky4": (0.0, 0.0, 0.0), 
            "LeftUpLeg": (95.592, 0.0, 0.0), 
            "LeftLeg": (-10.339, 0.0, 0.0), 
            "LeftFoot": (0.0, 0.0, 0.0), 
            "LeftToeBase": (0.0, 0.0, 0.0), 
            "LeftToe_End": (0.0, 0.0, 0.0), 
            "RightUpLeg": (95.592, 0.0, 0.0), 
            "RightLeg": (-10.339, 0.0, 0.0), 
            "RightFoot": (0.0, 0.0, 0.0), 
            "RightToeBase": (0.0, 0.0, 0.0), 
            "RightToe_End": (0.0, 0.0, 0.0), 
            }
        self.passengerCtrl = {}
        self.driverCtrl = {}


    def setPose(self) -> None:
        """ This is the main function.
        - Select locators
        - Get the joint name connected with the locator.
        - Check if the joint is a passenger or not, and if it has ctrl or not.
        - Finally, Set pose.
        """
        temp = self.getJointName()
        for loc, jntList in temp.items():
            for jnt in jntList:
                poseType = self.getPoseType(loc, jnt)
                self.setAttributes(jnt, poseType)


    def getJointName(self) -> dict:
        """ Returns the name of the joint 
        connected to the selected locator and constraintParent.
        >>> {"locatorName": [jointName1, jointName2, ...]}
        """
        sel = pm.selected()
        result = {}
        for i in sel:
            conn = list(set(pm.listConnections(i, type="parentConstraint")))
            for j in conn:
                jnt = list(set(pm.listConnections(j, type="joint")))
                result[i] = jnt
        return result


    def getPoseType(self, locator: str, joint: str) -> dict:
        """ PoseType has 4 cases
        - Passenger, bone only
        - Driver, bone only
        - Passenger, controller
        - Driver, controller
        """
        if not isinstance(locator, pm.PyNode):
            locator = pm.PyNode(locator)
        if not isinstance(joint, pm.PyNode):
            joint = pm.PyNode(joint)
        isPassenger = "passenger" in locator.stripNamespace()
        isCtrlType = pm.objExists(f"{joint.namespace()}cc_main")
        if isPassenger and isCtrlType:
            poseType = self.passengerCtrl
        elif not isPassenger and isCtrlType:
            poseType = self.driverCtrl
        elif isPassenger and not isCtrlType:
            poseType = self.passengerBone
        else:
            poseType = self.driverBone
        return poseType


    def setAttributes(self, jnt: str, poseType: dict) -> None:
        """ Bone type has the rotate values only.
        Ctrl type has the translate and rotate values.

        Example:
        - Bone Type -> {"Hips": (0, 0, 0), "Spine": (0, 0, 0), ...}
        - Ctrl Type -> {"cc_Hips": (0, 0, 0, 0, 0, 0), ...}
        """
        for name, attr in poseType.items():
            if len(attr) == 6:
                # The controller type has 6 attrs.
                pm.setAttr(f"{jnt.namespace()}{name}.translate", attr[:3])
                pm.setAttr(f"{jnt.namespace()}{name}.rotate", attr[3:])
            else:
                # The bone type has 3 attrs.
                pm.setAttr(f"{jnt.namespace()}{name}.rotate", attr)


    def setScaleLocator(self, size: int=300) -> None:
        loc = [i for i in pm.ls(type="transform") if "loc_vhcl_" in i.name()]
        for i in loc:
            pm.setAttr(f"{i}.scale", [size, size, size])


    def setScaleJoint(self, scl: float=1.0) -> None:
        temp = self.getJointName()
        for jntList in temp.values():
            for jnt in jntList:
                refName = jnt.namespace()
                mainCtrl = f"{refName}cc_main"
                isCtrlType = pm.objExists(mainCtrl)
                if isCtrlType:
                    pm.setAttr(f"{mainCtrl}.scale", (scl, scl, scl))
                else:
                    for name in self.passengerBone.keys():
                        pm.setAttr(f"{refName}{name}.scale", (scl, scl, scl))


pos = Pose()
pos.setPose()
# pos.setScaleJoint(0.8)