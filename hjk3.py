from typing import Callable, List, Tuple, Any # Union, Dict
# from collections import Counter
import time
import functools
# import math
# import re
import inspect
import maya.cmds as cmds
# import maya.api.OpenMaya as om2


__version__ = "Python 3.7.9"
__author__ = "HONG JINKI <hjk0314@gmail.com>"
__all__ = [
    'use_selection', 
    'alias', 
    'compare_execution_time', 

    'get_position', 
]


class Data:
    def __init__(self):
        """ This data class contains information such as the position 
        of the joint or the shape of the controller.
        
        ctrl_shapes
        -----------
            - A
                arch_two_line, arrow_plane, arrow_persp, arrow_circle, 
                arrow_cross, arrow_two_way, arrow_arch, arrow_L_shaped
            - C
                cap_half_sphere, car_body, car_bottom_sub, car_bottom_main, 
                circle_octagon, cone_triangle, cone_pyramid, cube, cross, 
                cylinder, 
            - D
                door_front, door_back
            - F
                foot_shoes, foot_box_type, foot_bear
            - H
                hat, head, hoof_horseshoe, hoof_simple_type
            - P
                pipe, plane_square, pointer_pin, pointer_rhombus, 
                pointer_circle, 
            - S
                scapula, sphere
            - T
                text_IKFK
         """
        self.ctrl_shapes = {
            "arch_two_line": [
                (-4, 0, 18), (4, 0, 18), (4, 12, 12.7), (4, 17, 0), 
                (4, 12, -12.7), (4, 0, -18), (-4, 0, -18), (-4, 12, -12.7), 
                (-4, 18, 0), (-4, 12, 12.7), (-4, 0, 18)
                ], 
            "arrow_plane": [
                (0, 0, 8), (8, 0, 4), (4, 0, 4), (4, 0, -8), 
                (-4, 0, -8), (-4, 0, 4), (-8, 0, 4), (0, 0, 8)
                ], 
            "arrow_persp": [
                (0, 3, 12), (12, 3, 6), (6, 3, 6), (6, 3, -12), 
                (-6, 3, -12), (-6, 3, 6), (-12, 3, 6), (0, 3, 12), 
                (0, -3, 12), (12, -3, 6), (6, -3, 6), (6, -3, -12), 
                (-6, -3, -12), (-6, -3, 6), (-12, -3, 6), (0, -3, 12), 
                (12, -3, 6), (12, 3, 6), (6, 3, 6), (6, 3, -12), 
                (6, -3, -12), (-6, -3, -12), (-6, 3, -12), (-6, 3, 6), 
                (-12, 3, 6), (-12, -3, 6)
                ], 
            "arrow_circle": [
                (14, 0, 0), (10, 0, -10), (0, 0, -14), (-10, 0, -10), 
                (-14, 0, 0), (-10, 0, 10), (0, 0, 14), (10, 0, 10), 
                (14, 0, 0), (10, 0, 4), (14, 0, 6), (14, 0, 0)
                ], 
            "arrow_cross": [
                (0, 0, -23.1), (-6.3, 0, -16.8), (-4.2, 0, -16.8), 
                (-4.2, 0, -12.6), (-10.5, 0, -10.5), (-12.6, 0, -4.2), 
                (-16.8, 0, -4.2), (-16.8, 0, -6.3), (-23.1, 0, 0), 
                (-16.8, 0, 6.3), (-16.8, 0, 4.2), (-12.6, 0, 4.2), 
                (-10.5, 0, 10.5), (-4.2, 0, 12.6), (-4.2, 0, 16.8), 
                (-6.3, 0, 16.8), (0, 0, 23.1), (6.3, 0, 16.8), 
                (4.2, 0, 16.8), (4.2, 0, 12.6), (10.5, 0, 10.5), 
                (12.6, 0, 4.2), (16.8, 0, 4.2), (16.8, 0, 6.3), 
                (23.1, 0, 0), (16.8, 0, -6.3), (16.8, 0, -4.2), 
                (12.6, 0, -4.2), (10.5, 0, -10.5), (4.2, 0, -12.6), 
                (4.2, 0, -16.8), (6.3, 0, -16.8), (0, 0, -23.1)
                ], 
            "arrow_two_way": [
                (-8, 0, -4), (8, 0, -4), (8, 0, -8), (16, 0, 0), 
                (8, 0, 8), (8, 0, 4), (-8, 0, 4), (-8, 0, 8), 
                (-16, 0, 0), (-8, 0, -8), (-8, 0, -4)
                ], 
            "arrow_arch": [
                (-0, 0, -12.6), (-0, 4, -13), (-0, 2, -10), 
                (-0, 0, -12.6), (-0, 2, -12), (-0, 6, -10), 
                (-0, 10, -6), (0, 12, 0), (0, 10, 6), (0, 6, 10), 
                (0, 2, 12), (0, 0, 12.6), (0, 2, 10), (0, 4, 13), 
                (0, 0, 12.6)
                ], 
            "arrow_L_shaped": [
                (0, 0, 0), (0, 6, 0), (0, 6, 3), 
                (1, 6, 2), (-1, 6, 2), (0, 6, 3), 
                ], 
            "cap_half_sphere": [
                (0, 0, 12), (-9, 0, 9), (-6.667, 6.667, 6.667), 
                (0, 9, 9), (6.667, 6.667, 6.667), (9, 0, 9), 
                (0, 0, 12), (0, 9, 9), (0, 12, 0), 
                (0, 9, -9), (0, 0, -12), (9, 0, -9), 
                (6.667, 6.667, -6.667), (0, 9, -9), (-6.667, 6.667, -6.667), 
                (-9, 0, -9), (0, 0, -12), (9, 0, -9), 
                (12, 0, 0), (9, 0, 9), (6.667, 6.667, 6.667), 
                (9, 9, 0), (6.667, 6.667, -6.667), (9, 0, -9), 
                (12, 0, 0), (9, 9, 0), (0, 12, 0), 
                (-9, 9, 0), (-6.667, 6.667, -6.667), (-9, 0, -9), 
                (-12, 0, 0), (-9, 9, 0), (-6.667, 6.667, 6.667), 
                (-9, 0, 9), (-12, 0, 0)
                ], 
            "car_body": [
                (81, 70, 119), (89, 56, 251), (89, -12, 251), 
                (89, -12, 117), (89, -12, -117), (89, -12, -229), 
                (81, 70, -229), (81, 70, -159), (69, 111, -105), 
                (69, 111, 63), (81, 70, 119), (-81, 70, 119), 
                (-89, 56, 251), (-89, -12, 251), (-89, -12, 117), 
                (-89, -12, -117), (-89, -12, -229), (-81, 70, -229), 
                (-81, 70, -159), (-69, 111, -105), (69, 111, -105), 
                (81, 70, -159), (-81, 70, -159), (-81, 70, -229), 
                (81, 70, -229), (89, -12, -229), (-89, -12, -229), 
                (-89, -12, -117), (-89, -12, 117), (-89, -12, 251), 
                (89, -12, 251), (89, 56, 251), (-89, 56, 251), 
                (-81, 70, 119), (-69, 111, 63), (-69, 111, -105), 
                (69, 111, -105), (69, 111, 63), (-69, 111, 63)
                ], 
            "car_bottom_sub": [
                (165, 0, -195), (0, 0, -276), (-165, 0, -195), (-165, 0, -0), 
                (-165, -0, 195), (-0, -0, 276), (165, -0, 195), (165, -0, 0), 
                (165, 0, -195)
                ], 
            "car_bottom_main": [
                (-92, 0, -300), (-193, 0, -200), (-193, 0, 0), 
                (-193, 0, 200), (-92, 0, 300), (92, 0, 300), 
                (193, 0, 200), (193, 0, 0), (193, 0, -200), 
                (92, 0, -300), (-92, 0, -300)
                ], 
            "circle_octagon": [
                (0, 0, -15), (-10, 0, -10), (-15, 0, 0), 
                (-10, 0, 10), (0, 0, 15), (10, 0, 10), 
                (15, 0, 0), (10, 0, -10), (0, 0, -15)
                ], 
            "cone_triangle": [
                (0, 10, 0), (-4.35, 0, 0), (4.35, 0, 0), (0, 10, 0), 
                (0, 0, 5), (-4.35, 0, 0), (4.35, 0, 0), (0, 0, 5)
                ], 
            "cone_pyramid": [
                (-5, 0, 0), (0, 0, 5), (5, 0, 0), (0, 0, -5), 
                (0, 10, 0), (-5, 0, 0), (0, 10, 0), (0, 0, 5), 
                (5, 0, 0), (0, 0, -5), (0, 0, -5), (-5, 0, 0), 
                (0, 0, 5), (5, 0, 0), (0, 10, 0)
                ], 
            "cube": [
                (-5, 5, -5), (-5, 5, 5), (5, 5, 5), (5, 5, -5), 
                (-5, 5, -5), (-5, -5, -5), (-5, -5, 5), (5, -5, 5), 
                (5, -5, -5), (-5, -5, -5), (-5, -5, 5), (-5, 5, 5), 
                (5, 5, 5), (5, -5, 5), (5, -5, -5), (5, 5, -5)
                ], 
            "cross": [
                (-1, 5, 0), (1, 5, 0), (1, 1, 0), (5, 1, 0), 
                (5, -1, 0), (1, -1, 0), (1, -5, 0), (-1, -5, 0), 
                (-1, -1, 0), (-5, -1, 0), (-5, 1, 0), (-1, 1, 0), 
                (-1, 5, 0)
                ], 
            "cylinder": [
                (-7, 7, 0), (-5, 7, 5), (0, 7, 7), (5, 7, 5), (7, 7, 0), 
                (5, 7, -5), (0, 7, -7), (0, 7, 7), (0, -7, 7), (-5, -7, 5), 
                (-7, -7, 0), (-5, -7, -5), (0, -7, -7), (5, -7, -5), 
                (7, -7, 0), (5, -7, 5), (0, -7, 7), (0, -7, -7), 
                (0, 7, -7), (-5, 7, -5), (-7, 7, 0), (7, 7, 0), 
                (7, -7, 0), (-7, -7, 0), (-7, 7, 0)
                ], 
            "door_front": [
                (0, 8, 0), (0, 58, -48), (0, 61, -100), (0, 8, -97), 
                (0, -45, -97), (0, -45, 0), (0, -16, 2), (0, 8, 0)
                ], 
            "door_back": [
                (0, 8, 0), (0, 58, -5), (0, 61, -73), (0, -4, -82), 
                (0, -45, -46), (0, -45, -2), (0, 8, 0)
                ], 
            "foot_shoes": [
                (-4, 0, -4), (-4, 0, -7), (-3, 0, -11), (-1, 0, -12), 
                (0, 0, -12), (1, 0, -12), (3, 0, -11), (4, 0, -7), 
                (4, 0, -4), (-4, 0, -4), (-5, 0, 1), (-5, 0, 6), 
                (-4, 0, 12), (-2, 0, 15), (0, 0, 15.5), (2, 0, 15), 
                (4, 0, 12), (5, 0, 6), (5, 0, 1), (4, 0, -4), (-4, 0, -4), 
                (4, 0, -4)
                ], 
            "foot_box_type": [
                (-6, 12, -14), (-6, 12, 6), (6, 12, 6), (6, 12, -14), 
                (-6, 12, -14), (-6, 0, -14), (-6, 0, 18), (6, 0, 18), 
                (6, 0, -14), (-6, 0, -14), (-6, 0, 18), (-6, 12, 6), 
                (6, 12, 6), (6, 0, 18), (6, 0, -14), (6, 12, -14)
                ], 
            "foot_bear": [
                (0, 0, 14.60237), (-3.77937, 0, 14.10481), 
                (-4.09646, 0, 15.28819), (-1.63552, 0, 17.47042), 
                (-0.97612, 0, 20.69277), (-3.15835, 0, 23.15371), 
                (-6.3807, 0, 23.81311), (-8.84164, 0, 21.63087), 
                (-9.50104, 0, 18.40853), (-7.31881, 0, 15.94759), 
                (-4.09646, 0, 15.28819), (-3.77937, 0, 14.10481), 
                (-7.30119, 0, 12.64603), (-10.32544, 0, 10.32544), 
                (-11.19173, 0, 11.19173), (-10.15162, 0, 14.31207), 
                (-11.19173, 0, 17.43241), (-14.31207, 0, 18.47252), 
                (-17.43241, 0, 17.43241), (-18.47252, 0, 14.31207), 
                (-17.43241, 0, 11.19173), (-14.31207, 0, 10.15162), 
                (-11.19173, 0, 11.19173), (-10.32544, 0, 10.32544), 
                (-12.64603, 0, 7.30119), (-14.10481, 0, 3.77937), 
                (-14.60237, 0, 0), (-14.10481, 0, -3.77937), 
                (-12.64602, 0, -7.30119), (-10.32543, 0, -10.32544), 
                (-7.30118, 0, -12.64602), (-3.77937, 0, -14.10481), 
                (0, 0, -14.60237), (3.77937, 0, -14.1048), 
                (7.30119, 0, -12.64602), (10.32543, 0, -10.32543), 
                (12.64602, 0, -7.30118), (14.1048, 0, -3.77937), 
                (14.60238, 0, 0), (14.10481, 0, 3.77937), 
                (12.64603, 0, 7.30119), (10.32544, 0, 10.32544), 
                (11.19173, 0, 11.19173), (14.31207, 0, 10.15162), 
                (17.43241, 0, 11.19173), (18.47252, 0, 14.31207), 
                (17.43241, 0, 17.43241), (14.31207, 0, 18.47252), 
                (11.19173, 0, 17.43241), (10.15162, 0, 14.31207), 
                (11.19173, 0, 11.19173), (10.32544, 0, 10.32544), 
                (7.30119, 0, 12.64603), (3.77937, 0, 14.10481), 
                (4.09646, 0, 15.28819), (7.31881, 0, 15.94759), 
                (9.50104, 0, 18.40853), (8.84164, 0, 21.63087), 
                (6.3807, 0, 23.81311), (3.15835, 0, 23.15371), 
                (0.97612, 0, 20.69277), (1.63552, 0, 17.47042), 
                (4.09646, 0, 15.28819), (3.77937, 0, 14.10481), 
                (0, 0, 14.60237), 
                ], 
            "hat": [
                (14, 9, 0), (0, 15, 0), (-14, 9, 0), (-7, -5, 0), 
                (-16, -7, 0), (0, -7, 0), (16, -7, 0), (7, -5, 0), 
                (14, 9, 0)
                ], 
            "head": [
                (13, 15, -11), (0, 25, -15), (-13, 15, -11), (-14, 6, 0), 
                (-13, 15, 11), (0, 25, 15), (13, 15, 11), (14, 6, 0), 
                (13, 15, -11)
                ], 
            "hoof_horseshoe": [
                (-6, 0, -5), (-6.5, 0, -1), (-6, 0, 3), (-5.2, 0, 5.5), 
                (-3, 0, 7.5), (0, 0, 8.2), (3, 0, 7.5), (5.2, 0, 5.5), 
                (6, 0, 3), (6.5, 0, -1), (6, 0, -5), (4, 0, -5), 
                (4.5, 0, -1), (4, 0, 3), (3.5, 0, 4.5), (2, 0, 6), 
                (0, 0, 6.5), (-2, 0, 6), (-3.5, 0, 4.5), (-4, 0, 3), 
                (-4.5, 0, -1), (-4, 0, -5), (-6, 0, -5), (-5.5, 0, -6.5), 
                (5.5, 0, -6.5), (4.5, 0, -10), (2.2, 0, -12.2), 
                (0, 0, -12.2), (-2.2, 0, -12.2), (-4.5, 0, -10), 
                (-5.5, 0, -6.5)
                ], 
            "hoof_simple_type": [
                (6, 6, -12), (0, 8, -12), (-6, 6, -12), (-8, 3, -13), 
                (-8, 0, -12), (-7, 0, -10), (-8, 0, -6), (-9, 0, -1), 
                (-8, 0, 4), (-5, 0, 9), (0, 0, 10), (5, 0, 9), (8, 0, 4), 
                (9, 0, -1), (8, 0, -6), (7, 0, -10), (8, 0, -12), 
                (8, 3, -13), (6, 6, -12)
                ], 
            "text_IKFK": [
                (-6.611, 0, 2), (-6.611, 0, -2), (-5.792, 0, -2), 
                (-5.792, 0, 2), (-6.611, 0, 2), (-4.692, 0, 2), 
                (-4.692, 0, -2), (-3.879, 0, -2), (-3.879, 0, -0.368), 
                (-2.391, 0, -2), (-1.342, 0, -2), (-2.928, 0, -0.358), 
                (-1.245, 0, 2), (-2.304, 0, 2), (-3.495, 0, 0.245), 
                (-3.879, 0, 0.65), (-3.879, 0, 2), (-4.692, 0, 2), 
                (-0.376, 0, 2), (-0.376, 0, -2), (2.401, 0, -2), 
                (2.401, 0, -1.294), (0.442, 0, -1.294), (0.442, 0, -0.384), 
                (2.156, 0, -0.384), (2.156, 0, 0.322), (0.442, 0, 0.322), 
                (0.442, 0, 2), (-0.376, 0, 2), (3.164, 0, 2), 
                (3.164, 0, -2), (3.977, 0, -2), (3.977, 0, -0.368), 
                (5.465, 0, -2), (6.513, 0, -2), (4.928, 0, -0.358), 
                (6.611, 0, 2), (5.552, 0, 2), (4.36, 0, 0.245), 
                (3.977, 0, 0.65), (3.977, 0, 2), (3.164, 0, 2), 
                (6.611, 0, 2)
                ], 
            "pipe": [
                (0, 7, 7), (0, -7, 7), (4.9, -7, 4.9), (7, -7, 0), 
                (7, 7, 0), (4.9, 7, -4.9), (0, 7, -7), (0, -7, -7), 
                (-4.9, -7, -4.9), (-7, -7, 0), (-7, 7, 0), (-4.9, 7, 4.9), 
                (0, 7, 7), (4.9, 7, 4.9), (7, 7, 0), (7, -7, 0), 
                (4.9, -7, -4.9), (0, -7, -7), (0, 7, -7), (-4.9, 7, -4.9), 
                (-7, 7, 0), (-7, -7, 0), (-4.9, -7, 4.9), (0, -7, 7)
                ], 
            "plane_square": [
                (25, 0, 25), (25, 0, -25), (-25, 0, -25), 
                (-25, 0, 25), (25, 0, 25)
                ], 
            "pointer_pin": [
                (0, 8, 4), (-2.8, 8, 2.8), (-4, 8, 0), (-2.8, 8, -2.8), 
                (0, 8, -4), (2.8, 8, -2.8), (4, 8, -0), (2.8, 8, 2.8), 
                (0, 8, 4), (0, 8, -0), (0, 0, -0)
                ], 
            "pointer_rhombus": [
                (0, 0, 0), (0, 4, 0), (0, 5, 1), (0, 6, 0), 
                (0, 5, -1), (0, 4, 0), 
                ], 
            "pointer_circle": [
                (0, 0, 0), (0, 4, 0), (0, 4.586, 1.414), 
                (0, 6, 2), (0, 7.586, 1.414), (0, 8, 0), 
                (0, 7.586, -1.414), (0, 6, -2), (0, 4.586, -1.414), 
                (0, 4, 0), 
                ], 
            "scapula": [
                (2.4, 9.5, -15), (0, 0, -18), (-2.4, 9.5, -15), (-4, 17, 0), 
                (-2.4, 9.5, 15), (0, 0, 18), (2.4, 9.5, 15), (4, 17, 0), 
                (2.4, 9.5, -15)
                ], 
            "sphere": [
                (0, 5, 0), (0, 3.5, 3.5), (0, 0, 5), (0, -3.5, 3.5), 
                (0, -5, 0), (0, -3.5, -3.5), (0, 0, -5), (0, 3.5, -3.5), 
                (0, 5, 0), (-3.5, 3.5, 0), (-5, 0, 0), (-3.5, 0, 3.5), 
                (0, 0, 5), (3.5, 0, 3.5), (5, 0, 0), (3.5, 0, -3.5), 
                (0, 0, -5), (-3.5, 0, -3.5), (-5, 0, 0), (-3.5, -3.5, 0), 
                (0, -5, 0), (3.5, -3.5, 0), (5, 0, 0), (3.5, 3.5, 0), 
                (0, 5, 0)
                ], 
            "square": [
                (25, 0, 25), (25, 0, -25), (-25, 0, -25), 
                (-25, 0, 25), (25, 0, 25)
                ], 
        }
        self.char_joints = {}
        self.color_chart = {
            "gray": (0.534, 0.534, 0.534), 
            "black": (0.0, 0.0, 0.0), 
            "dark_gray": (0.332, 0.332, 0.332), 
            "medium_gray": (0.662, 0.662, 0.662), 
            "brick_red": (0.607, 0.258, 0.234), 
            "indigo": (0.17, 0.095, 0.44), 
            "blue": (0.0, 0.0, 1.0), 
            "olive_green": (0.242, 0.345, 0.184), 
            "dark_violet": (0.209, 0.096, 0.334), 
            "light_purple": (0.744, 0.33, 0.871), 
            "brown": (0.55, 0.384, 0.287), 
            "dark_brown": (0.299, 0.217, 0.189), 
            "rust": (0.595, 0.297, 0.118), 
            "red": (1.0, 0.0, 0.0), 
            "lime_green": (0.0, 1.0, 0.0), 
            "periwinkle": (0.295, 0.336, 0.645), 
            "white": (1.0, 1.0, 1.0), 
            "yellow": (1.0, 1.0, 0.0), 
            "light_cyan": (0.673, 1.0, 1.0), 
            "pale_green": (0.616, 1.0, 0.648), 
            "light_pink": (1.0, 0.78, 0.761), 
            "peach": (1.0, 0.76, 0.545), 
            "chartreuse": (0.840, 1.0, 0.0), 
            "forest_green": (0.443, 0.645, 0.426), 
            "tan": (0.631, 0.497, 0.291), 
            "khaki": (0.675, 0.693, 0.324), 
            "sage_green": (0.548, 0.683, 0.324), 
            "moss_green": (0.476, 0.679, 0.455), 
            "teal_blue": (0.49, 0.68, 0.695), 
            "slate_blue": (0.392, 0.469, 0.683), 
            "lavender_gray": (0.468, 0.304, 0.678), 
            "rose": (0.608, 0.333, 0.478), 
        }


def use_selection(func):
    """ Decorator to pass selected objects as item to the wrapped function.

    This decorator modifies the behavior of a function 
    such that if no arguments are explicitly provided when 
    calling the wrapped function, it attempts to pass the currently 
    selected objects (from `cmds.ls(fl=True, os=True)`) as arguments.

    The behavior depends on the decorated function's signature:
    - If the function accepts variable positional arguments (`*args`), 
      all selected objects will be passed as individual positional arguments.
    - If the function accepts exactly one positional argument, 
      it will be called for each selected object, 
      and the results will be returned in a dictionary where 
      keys are the selected objects and values are the func's return values.
    - Otherwise, if the function accepts a fixed number of positional args,
      the decorator will pass the first `n` selected objects, where
      `n` is the number of positional arguments the function expects.

    If no objects are selected and no arguments are provided, 
    a warning will be issued.

    Args:
        func (callable): The function to be wrapped.

    Returns:
        callable: The wrapped function with selection handling capabilities.

    Raises:
        RuntimeWarning: If nothing is selected and no arguments are passed.

    Examples:
        >>> @use_selection
        >>> func(*args)
        ...
        >>> @use_selection
        >>> func(obj)
        ...
        >>> @use_selection
        >>> func(item1, item2)
        ...
        >>> @use_selection
        >>> func(arg1, arg2="default")
     """
    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    has_varargs = any(
        p.kind == inspect.Parameter.VAR_POSITIONAL for p in params
    )
    positional_arg = [
        p 
        for p in params 
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]
    num_positional_arg = len(positional_arg)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            return func(*args, **kwargs)

        sel = cmds.ls(fl=True, os=True)

        if not sel:
            cmds.warning("Nothing is selected.")
            return

        if has_varargs:
            return func(*sel, **kwargs)
        elif num_positional_arg == 1:
            result = {}
            for i in sel:
                result[i] = func(i, **kwargs)
            return result
        else:
            return func(*sel[:num_positional_arg], **kwargs)

    return wrapper


def alias(**alias_map):
    """ Decorator to allow aliasing of keyword args when calling a function.

    This decorator enables alternate (shortened or customized) 
    keyword arguments to be mapped to the actual parameter names 
    defined in the function signature.

    Args
    ----
    alias_map : dict
        A dictionary mapping alias names (str) to actual parameter names. 
        For example: {'a': 'x', 'b': 'y'}

    Returns
    -------
    function : 
        A wrapped version of the original function that resolves
        aliases before calling it.

    Example
    -------
    >>> @alias(rx='rangeX', ry='rangeY', rz='rangeZ')
    >>> func(rx=[0, 0, 0, 0], ry=[0, 0, 0, 0])
    ...
    >>> @alias(t="translate", r="rotate", s="sclae", v="visibility")
    >>> func(t=True, r=True, s=True, v=True)
     """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            resolved_kwargs = {
                alias_map.get(k, k): v for k, v in kwargs.items()
            }
            return func(*args, **resolved_kwargs)
        
        return wrapper
    
    return decorator


def compare_execution_time(
    func1: Callable,
    func2: Callable,
    *args: Any,
    **kwargs: Any
) -> Tuple[float, float]:
    """ Measure and compare the execution time of two functions with the 
    same arguments.

    This function executes `func1` and `func2` in sequence, passing them 
    the same positional and keyword arguments, and returns their execution 
    durations in seconds.

    Args:
        func1 (Callable): The first function to measure.
        func2 (Callable): The second function to measure.
        *args: Positional arguments to pass to both functions.
        **kwargs: Keyword arguments to pass to both functions.

    Returns:
        tuple[float, float]: 
            A tuple containing (duration_func1, duration_func2), each in sec.

    Examples:
        >>> compare_execution_time(func1, func2, "pSphere1.vtx[257])
        (0.05010910000055446, 0.03423800000018673)
     """
    start1 = time.perf_counter()
    func1(*args, **kwargs)
    end1 = time.perf_counter()

    start2 = time.perf_counter()
    func2(*args, **kwargs)
    end2 = time.perf_counter()

    return (end1 - start1, end2 - start2)


def get_position(obj_or_vtx: str) -> tuple:
    """ Get the coordinates of an object or point. ``**No Decrations.**``
    
    Args:
        obj_or_vtx (str): The name of the object or vertex component (e.g., "pSphere1" or "pSphere1.vtx[317]").

    Raises:
        ValueError: If the specified object or vertex does not exist.
        ValueError: If a transform node is not found for the given object.

    Returns:
        tuple: A tuple of three floating-point numbers (x, y, z) representing the world-space coordinates.

    Examples:
        >>> get_position("pSphere1")
        (0.0, 0.0, 0.0)
        >>> get_position("pSphere1.vtx[317]")
        (64.60261, 67.08806, -62.83971)
    """
    items: List[str] = cmds.ls(obj_or_vtx, flatten=True) or []
    if not items:
        raise ValueError(f"Non-existent {obj_or_vtx}")
    target = items[0]

    def is_component(name: str) -> bool:
        return ("." in name) and ("[" in name and "]" in name)

    if is_component(target):
        pos = cmds.pointPosition(target, world=True)
    else:
        dag = target
        if not cmds.objectType(dag, isAType="transform"):
            parents = cmds.listRelatives(dag, parent=True, path=True) or []
            if parents and cmds.objectType(parents[0], isAType="transform"):
                dag = parents[0]
            else:
                raise ValueError(f"Transform node not found: {target}")
        pos = cmds.xform(dag, q=True, ws=True, rp=True)

    return tuple(round(float(v), 5) for v in pos)


