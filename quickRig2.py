
import pymel.core as pm


joint = {
    "root": {
        'jnt_root': (0.0, 91.146, -2.311), 
        'jnt_spine_1': (-0.0, 101.79, -0.828), 
        'jnt_spine_2': (-0.0, 112.04, -0.291), 
        'jnt_spine_3': (-0.0, 121.978, -0.795), 
        'jnt_spine_4': (-0.0, 130.703, -2.506), 
        'jnt_neck_1': (-0.0, 139.579, -5.133), 
        'jnt_neck_2': (-0.0, 143.202, -3.147), 
        'jnt_head': (-0.0, 151.415, -0.776), 
        'jnt_head_end': (-0.0, 164.146, -0.776), 
    }, 
    "arm_L": {
        'jnt_scapula_L': (7.581, 133.499, -4.058), 
        'jnt_shoulder_L': (16.671, 129.738, -3.624), 
        'jnt_elbow_L': (41.006, 127.424, -4.551), 
        'jnt_wrist_L': (66.078, 125.041, -4.841), 
        'jnt_parm_L': (71.356, 124.058, -4.841), 
    }, 
    "arm_R": {
        'jnt_scapula_R': (-7.581, 133.499, -4.058), 
        'jnt_shoulder_R': (-16.671, 129.738, -3.624), 
        'jnt_elbow_R': (-41.018, 127.428, -3.083), 
        'jnt_wrist_R': (-66.062, 125.053, -1.862), 
        'jnt_parm_R': (-71.332, 124.072, -1.542), 
    }, 
    "leg_L": {
        'jnt_hip_L': (10.968, 82.407, -0.453), 
        'jnt_knee_L': (16.924, 45.846, -3.606), 
        'jnt_ankle_L': (22.447, 9.76, -8.165), 
        'jnt_ball_L': (26.036, 1.972, 0.594), 
        'jnt_toe_L': (28.191, 0.807, 8.479), 
    }, 
    "leg_R": {
        'jnt_hip_R': (-10.968, 82.407, -0.453), 
        'jnt_knee_R': (-16.924, 45.846, -3.606), 
        'jnt_ankle_R': (-22.447, 9.76, -8.165), 
        'jnt_ball_R': (-26.036, 1.972, 0.594), 
        'jnt_toe_R': (-28.191, 0.807, 8.479), 
    }, 
    "thumb_L": {
        'jnt_thumb_L_1': (69.91, 123.216, -2.033), 
        'jnt_thumb_L_2': (71.54, 122.745, -0.221), 
        'jnt_thumb_L_3': (73.169, 122.275, 1.591), 
        'jnt_thumb_L_4': (74.799, 121.804, 3.403), 
    }, 
    "index_L": {
        'jnt_index_L_1': (74.697, 123.363, -2.847), 
        'jnt_index_L_2': (77.057, 123.282, -2.082), 
        'jnt_index_L_3': (79.417, 123.2, -1.318), 
        'jnt_index_L_4': (81.777, 123.119, -0.554), 
    }, 
    "middle_L": {
        'jnt_middle_L_1': (75.236, 123.622, -4.757), 
        'jnt_middle_L_2': (77.686, 123.756, -5.131), 
        'jnt_middle_L_3': (80.136, 123.89, -5.505), 
        'jnt_middle_L_4': (82.586, 124.024, -5.879), 
    }, 
    "ring_L": {
        'jnt_ring_L_1': (74.493, 123.638, -6.872), 
        'jnt_ring_L_2': (76.421, 123.986, -8.153), 
        'jnt_ring_L_3': (78.348, 124.335, -9.434), 
        'jnt_ring_L_4': (80.275, 124.683, -10.716), 
    }, 
    "pinky_L": {
        'jnt_pinky_L_1': (72.929, 123.458, -8.344), 
        'jnt_pinky_L_2': (73.702, 123.805, -9.991), 
        'jnt_pinky_L_3': (74.475, 124.153, -11.637), 
        'jnt_pinky_L_4': (75.247, 124.501, -13.284), 
    }, 
    "thumb_R": {
        'jnt_thumb_R_1': (-70.239, 123.472, 1.438), 
        'jnt_thumb_R_2': (-71.716, 123.13, 3.402), 
        'jnt_thumb_R_3': (-73.194, 122.788, 5.367), 
        'jnt_thumb_R_4': (-74.671, 122.448, 7.332), 
    }, 
    "index_R": {
        'jnt_index_R_1': (-74.746, 123.923, 0.801), 
        'jnt_index_R_2': (-77.065, 123.821, 1.678), 
        'jnt_index_R_3': (-79.385, 123.718, 2.555), 
        'jnt_index_R_4': (-81.705, 123.616, 3.432), 
    }, 
    "middle_R": {
        'jnt_middle_R_1': (-75.541, 123.844, -1.26), 
        'jnt_middle_R_2': (-78.019, 123.951, -1.366), 
        'jnt_middle_R_3': (-80.496, 124.056, -1.472), 
        'jnt_middle_R_4': (-82.974, 124.162, -1.578), 
    }, 
    "ring_R": {
        'jnt_ring_R_1': (-74.697, 123.749, -3.267), 
        'jnt_ring_R_2': (-76.68, 123.701, -4.508), 
        'jnt_ring_R_3': (-78.664, 123.653, -5.75), 
        'jnt_ring_R_4': (-80.647, 123.605, -6.991), 
    }, 
    "pinky_R": {
        'jnt_pinky_R_1': (-72.958, 123.528, -4.738), 
        'jnt_pinky_R_2': (-73.615, 123.304, -6.454), 
        'jnt_pinky_R_3': (-74.272, 123.081, -8.171), 
        'jnt_pinky_R_4': (-74.929, 122.857, -9.888)
    }, 
}


def createJoint():
    
    jnt = []
    for i in joint:
        pm.select(cl=True)
        for k, v in i.items():
            pm.joint(p=(0, 0, 0), n=k, rad=10)
            pm.move(k, v)
        jnt.append(list(i.keys()))
    return jnt


def orientJnt(jntList: list):
    """ Freeze and Orient joints
    Select only "joint", freeze and orient. 
    And the end joints inherit the orient of the parent joint.
     """
    pm.select(cl=True)
    # freeze joints
    pm.makeIdentity(jntList, a=True, jo=True, n=0)
    init = jntList[0]
    last = jntList[-1]
    # orient joints
    pm.joint(init, e=True, oj='xyz', sao='yup', ch=True, zso=True)
    # orient end joints
    pm.joint(last, e=True, oj='none', ch=True, zso=True)


jntList = createJoint()
for i in jntList:
    orientJnt(i)

