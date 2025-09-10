# -*- coding: utf-8 -*-


from typing import Dict, List, Tuple, Union
# from collections import Counter
import time
import functools
import math
import re
import inspect
import maya.cmds as cmds
import maya.api.OpenMaya as om2


__version__ = "Python 3.7.9"
__author__ = "HONG JINKI <hjk0314@gmail.com>"
__all__ = [
    'with_selection', 
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
                circle, cone_triangle, cone_pyramid, cube, cross, 
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
            "circle": [
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



def with_selection(func):
    """ Use this function as a decoration when you want to pass the selection as an argument to a function.

    Examples
    --------
    >>> @with_selection
    >>> func(*args)
    ...
    >>> @with_selection
    >>> func(item1, item2)
    ...
    >>> @with_selection
    >>> func(arg1, arg2="default")
    """
    sig = inspect.signature(func)
    params = list(sig.parameters.values())


    is_arg = any(p.kind==inspect.Parameter.VAR_POSITIONAL for p in params)
    positional_arg = [p for p in params 
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
    num_positional_arg = len(positional_arg)


    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            return func(*args, **kwargs)


        sel = cmds.ls(fl=True, os=True)
        if not sel:
            cmds.warning("Nothing is selected.")
            return


        if is_arg:
            return func(*sel, **kwargs)
        # elif num_positional_arg == 1:
        #     result = {}
        #     for i in sel:
        #         result[i] = func(i, **kwargs)
        #     return result
        else:
            return func(*sel[:num_positional_arg], **kwargs)

    return wrapper



def alias(**alias_map):
    """ A decorator that maps aliases to keyword arguments.

    Examples
    --------
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



def compare_execution_time(func1, func2, *args, **kwargs) -> Tuple:
    """ Compare the execution time of two functions with the same arguments.

    Examples:
    >>> compare_execution_time(func1, func2, "pSphere1.vtx[257])
    (0.0501091, 0.0342380)
    """
    start1 = time.perf_counter()
    func1(*args, **kwargs)
    end1 = time.perf_counter()


    start2 = time.perf_counter()
    func2(*args, **kwargs)
    end2 = time.perf_counter()


    return (end1 - start1, end2 - start2)



@with_selection
def get_position(*args: str) -> List[Tuple]:
    """ Get the world-space coordinates of multiple objects or vertices.

    Args
    ----
        *args(str) : object or vertex

    Notes
    -----
        **Decoration** : @with_selection

    Examples
    --------
    >>> get_positions()
    >>> get_positions("test_sphere", "test_sphere.vtx[100]")
    [(0.0, 0.0, 0.0), (3.63223, 2.59367, -2.59367)]
    """
    results = []
    for obj_or_vtx in args:
        items = cmds.ls(obj_or_vtx, flatten=True) or []
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
                parents = cmds.listRelatives(dag, p=True, path=True) or []
                is_transform = cmds.objectType(parents[0], isa="transform")
                if parents and is_transform:
                    dag = parents[0]
                else:
                    raise ValueError(f"Transform node not found: {target}")
            pos = cmds.xform(dag, q=True, ws=True, rp=True)

        results.append(tuple(round(float(v), 5) for v in pos))

    return results



@with_selection
def get_bounding_box_position(*args) -> List[Tuple]:
    """ Get the coordinates of the center pivot of the boundingBox.

    Notes
    -----
        **Decoration** : @with_selection

    Examples
    --------
    >>> get_bounding_box_position("pCube1", "pSphere1", "pCylinder1")
    >>> get_bounding_box_position("pCube1.vtx[5]", "pSphere1.vtx[218]")
    >>> get_bounding_box_position()
    (-0.70783, 1.6044, -1.28288)
    """
    try:
        bbox = cmds.exactWorldBoundingBox(args[0])
    except RuntimeError:
        print(f"Error: Invalid object name '{args[0]}'")
        return None


    xmin, ymin, zmin, xmax, ymax, zmax = bbox
    for obj in args[1:]:
        try:
            current_bbox = cmds.exactWorldBoundingBox(obj)
            xmin = min(xmin, current_bbox[0])
            ymin = min(ymin, current_bbox[1])
            zmin = min(zmin, current_bbox[2])
            xmax = max(xmax, current_bbox[3])
            ymax = max(ymax, current_bbox[4])
            zmax = max(zmax, current_bbox[5])
        except RuntimeError:
            print(f"Warning: Skipping invalid object name '{obj}'")
            continue


    center_x = (xmin + xmax) / 2.0
    center_y = (ymin + ymax) / 2.0
    center_z = (zmin + zmax) / 2.0

    result = tuple(round(float(v), 5) for v in [center_x, center_y, center_z])
    
    return result



@with_selection
def get_bounding_box_size(*args) -> List[Tuple]:
    """ Get the size the boundingBox.

    Notes
    -----
        **Decoration** : @with_selection

    Examples
    --------
    >>> get_bounding_box_size("pCube1", "pSphere1", "pCylinder1")
    >>> get_bounding_box_size("pCube1.vtx[5]", "pSphere1.vtx[218]")
    >>> get_bounding_box_size()
    (64.60261, 67.08806, -62.83971)
    """
    try:
        bbox = cmds.exactWorldBoundingBox(args[0])
    except RuntimeError:
        print(f"Error: Invalid object name '{args[0]}'")
        return None


    xmin, ymin, zmin, xmax, ymax, zmax = bbox
    for obj in args[1:]:
        try:
            current_bbox = cmds.exactWorldBoundingBox(obj)
            xmin = min(xmin, current_bbox[0])
            ymin = min(ymin, current_bbox[1])
            zmin = min(zmin, current_bbox[2])
            xmax = max(xmax, current_bbox[3])
            ymax = max(ymax, current_bbox[4])
            zmax = max(zmax, current_bbox[5])
        except RuntimeError:
            print(f"Warning: Skipping invalid object name '{obj}'")
            continue


    center_x = (xmax - xmin) / 2.0
    center_y = (ymax - ymin) / 2.0
    center_z = (zmax - zmin) / 2.0

    result = tuple(round(float(v), 5) for v in [center_x, center_y, center_z])
    
    return result



def get_flatten_list(data: Union[dict, list], seen=None) -> list:
    """ Flattens a list within a list. 

    Notes
    -----
        **No Decoration**

    Examples
    --------
    >>> get_flatten_list({'a': {'b': {'c': 1}, 'd': 2}})
    ['a', 'b', 'c', 1, 'd', 2]
    >>> get_flatten_list(["a", ["b"], ["c"]], [[["d"], "e"], "f"], ...)
    ['a', 'b', 'c', 'd', 'e', 'f']
    """
    if seen is None:
        seen = set()


    result = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key not in seen:
                seen.add(key)
                result.append(key)
            result.extend(get_flatten_list(value, seen))
    elif isinstance(data, list):
        for item in data:
            result.extend(get_flatten_list(item, seen))
    else:
        if data not in seen:
            seen.add(data)
            result.append(data)

    return result



def get_distance(
        point1: Union[tuple, list], 
        point2: Union[tuple, list]) -> float:
    """ Returns the distance between the two coordinates.

    Notes
    -----
        **No Decoration**
    
    Examples
    --------
    >>> get_distance([0,0,0], [1,2,3])
    3.74166
     """
    result = math.sqrt(sum((a - b)**2 for a, b in zip(point1, point2)))
    result = round(result, 5)

    return result



def get_referenced_list() -> list:
    """ Returns a list of groups of referenced nodes using cmds.

    Notes
    -----
        **No Decoration**
    
    Examples
    --------
    >>> get_referenced_list()
    ['vhcl_bestaB_mdl_v9999:bestaB', ...]
    """
    references = cmds.file(query=True, reference=True)
    if not references:
        return []


    result = []
    for ref_path in references:
        nodes = cmds.referenceQuery(ref_path, nodes=True)
        if nodes:
            result.append(nodes[0])


    return result



@with_selection
def get_range_path(start_jnt: str, end_jnt: str) -> list:
    """ Get the range ``joints`` or ``objects`` 
    from the start joint to the end joint. The end is included.

    Notes
    -----
        **Decoration** : @with_selection

    Structure
    ---------
    joint1
        joint2
            joint3
                joint4
                    joint5
            joint8
                joint9
                    joint10
                        joint11

    Examples
    --------
    >>> get_range_path('joint2', 'joint10')
    ['joint2', 'joint3', 'joint8', 'joint9', 'joint10']
    """
    if not cmds.objExists(start_jnt):
        raise ValueError(f"'{start_jnt}' does not exist.")
    if not cmds.objExists(end_jnt):
        raise ValueError(f"'{end_jnt}' does not exist.")


    path = []
    current = end_jnt
    while current != start_jnt:
        path.append(current)
        parent_nodes = cmds.listRelatives(current, p=True, f=False)
        if not parent_nodes:
            raise ValueError(f"'{current}' cannot reach '{start_jnt}'.")
        parent = parent_nodes[0]
        current = parent


    path.append(start_jnt)
    path.reverse()
    
    return path



@alias(p="primary", s="secondary")
@with_selection
def orient_joint(joint, **kwargs) -> None:
    """ This function first freezes the joint and then orients the joint.
    
    Notes
    -----
        **Decoration**
            - @alias(p="primary", s="secondary")

    Args
    ----
        *args : str
            - joint1, joint2, joint3 ...
        kwargs: 
            - Maya default: xyz, yup
            - Mixamo: yzx, zup
            - Left hand: yxz, zdown

    Examples
    --------
    >>> orient_joint(p="yzx", s="zup") # Mixamo
    >>> orient_joint(p="yxz", s="zdown") # Left hand
    >>> orient_joint(p="xyz", s="yup") # Default
    ...
    >>> orient_joint() # @with_selection
    >>> orient_joint("joint1", "joint4")
    >>> orient_joint(*["joint1", "joint2"], p="yzx", s="zup")
    """
    valid_primary = {"xyz", "yzx", "zxy", "zyx", "yxz", "xzy", "none"}
    valid_secondary = {"xup", "xdown", "yup", "ydown", "zup", "zdown", "none"}
    primary = "xyz"
    secondary = "yup"

    for k, v in kwargs.items():
        if k == "primary" and v in valid_primary:
            primary = v
        elif k == "secondary" and v in valid_secondary:
            secondary = v
        else:
            cmds.warning(f"Ignored invalid flag: {k}={v}")

    cmds.makeIdentity(joint, apply=True, jointOrient=True, normal=False)

    cmds.joint(
            joint, 
            edit=True,
            children=True,
            zeroScaleOrient=True,
            orientJoint=primary,
            secondaryAxisOrient=secondary
        )

    end_joints = []
    for j in cmds.listRelatives(joint, ad=True):
        if not cmds.listRelatives(j, children=True, type="joint"):
            end_joints.append(j)
    for ej in end_joints:
        cmds.joint(ej, e=True, oj='none', ch=True, zso=True)



@with_selection
def create_pole_vector_joints(*args) -> list:
    """ This function finds the pole vector direction of a joint.

    It creates two joints connecting the beginning and end of the three selected joints, rotates them 90 degrees, and places them at the center of the three selected joints.

    Notes
    -----
        **Decoration** : @with_selection

    Args
    ----
        - joints : str
            joint1, joint2, joint3, joint4, joint5 ...

    Examples
    --------
    >>> create_pole_vector_joints() # @with_selection
    >>> create_pole_vector_joints("joint1", "joint2", "joint3")
    >>> create_pole_vector_joints(*["joint1", "joint2", "joint3"])
    ["joint1", "joint2"]
    """
    if len(args) < 3:
        cmds.warning("At least 3 joints are required.")
        return


    jnt_pos = [cmds.xform(i, q=True, ws=True, rp=True) for i in args]
    mid_jnt = args[int(len(args)/2)]
    end_jnt = args[-1]


    cmds.select(cl=True)
    result = []
    for pos in jnt_pos[::2]:
        jnt_name = cmds.joint(p=pos) 
        result.append(jnt_name)


    pj = result[0]
    cmds.joint(pj, e=True, ch=False, zso=True, oj="xyz", sao="yup")
    cmds.aimConstraint(end_jnt, pj, o=(0, 0, 90), wut='object', wuo=mid_jnt)
    cmds.delete(pj, cn=True)
    cmds.matchTransform(pj, mid_jnt, pos=True)

    return result



@with_selection
def parent_in_sequence(*args) -> list:
    """ Parent given nodes hierarchically in sequence.

    If no arguments are provided, use the current selection. Each node will become the parent of the next one in order.

    Notes
    -----
        **Decoration** : @with_selection

    Args
    ----
        - object : str

    Examples
    --------
    >>> parent_in_sequence() # @with_selection
    >>> parent_in_sequence('joint1', 'joint2', 'joint3', ...)
    >>> parent_in_sequence(*['joint1', 'joint2', 'joint3', ...])
    ['joint1', 'joint2', 'joint3', ...]
    """
    result = []
    for obj, child in zip(args, args[1:]):
        result.append(obj)
        try:
            cmds.parent(child, obj)
        except RuntimeError as e:
            cmds.warning(e)


    if args:
        result.append(args[-1])

    return result



@with_selection
def group_with_pivot(*args, **kwargs) -> List[list]:
    """ Create a group that includes ownself while maintaining own pivot position.

    Notes
    -----
        **Decoration** : @with_selection

    Examples
    --------
    >>> group_with_pivot() # @with_selection
    >>> group_with_pivot('pCube1', 'pCube2', 'pCube3',...)
    >>> group_with_pivot('p1', 'p2', null=True)
    [['p1_grp', 'p1_null', 'p1'], ['p2_grp', 'p2_null', 'p2'], ...]
    """
    result = []
    for i in args:
        grp_name = [f"{i}_grp"]
        if kwargs.get("null", False):
            grp_name.append(f"{i}_null")


        groups = []
        for gn in grp_name:
            gn = "" if cmds.objExists(gn) else gn
            grp = cmds.group(em=True, n=gn)
            cmds.matchTransform(grp, i, pos=True, rot=True)
            groups.append(grp)
        groups.append(i)


        top_group = cmds.listRelatives(i, parent=True, fullPath=False)
        if top_group:
            cmds.parent(groups[0], top_group)


        parent_in_sequence(*groups)
        result.append(groups)

    return result



@alias(s="style")
@with_selection
def set_joint_style(*args, style: str="bone") -> None:
    """ Set the drawing style of the specified joints.

    Notes
    -----
        **Decoration** :
            - @with_selection
            - @alias(s="style")

    Args
    ----
        - joints : str
        - style : str, optional
            - **bone**: (0)
            - **multiChild as box**: (1)
            - **none**: (2)

    Examples
    --------
    >>> set_joint_style()
    >>> set_joint_style("joint1", style="bone")
    >>> set_joint_style(style="none")
    """
    style_map = {
        "bone": 0,
        "multiChild": 1,
        "none": 2,
    }


    draw_style = style_map.get(style, 0)
    for i in args:
        cmds.setAttr(f"{i}.drawStyle", draw_style)



@with_selection
def get_connected_nodes(node: str) -> list:
    """ Returns the names of connected nodes.

    Notes
    -----
        **Decoration** :
            - @with_selection

    Args
    ----
        - node : str

    Examples
    --------
    >>> get_connected_nodes()
    >>> get_connected_nodes("joint1", ...)
    ['addDoubleLinear1', 'addDoubleLinear2', 'motionPath1', ...]
    """
    if not cmds.objExists(node):
        return []

    targets = set()
    conn = cmds.listConnections(node, s=True, d=True) or []
    for n in conn:
        if n != node and n != "time1" and not n.startswith("default"):
            targets.add(n)

    return list(targets)



@alias(c="curve", n="num_of_jnt")
def create_joint_on_curve_path(curve: str, num_of_jnt: int=1) -> list:
    """ This function creates a few number of joints on a curve. Using the motion path, finally, it deletes the nodes related to the motion path.

    Notes
    -----
        **Decoration** :
            - @alias(c="curve", n="num_of_jnt")

    Args
    ----
        - curve : str
        - num_of_jnt : int

    Examples
    --------
    >>> create_joint_on_curve_path("curve", n=5)
    ["joint1", "joint2", "joint3", ...]
    """
    if not isinstance(num_of_jnt, int) or num_of_jnt < 1:
        cmds.warning("Parameter 'num' must be a positive integer.")
        return []

    if not cmds.objExists(curve):
        cmds.warning(f"Curve '{curve}' does not exist.")
        return []

    step = 1.0/(num_of_jnt-1) if num_of_jnt > 1 else 0.0
    result = []
    for i in range(num_of_jnt):
        cmds.select(cl=True)
        jnt = cmds.joint(p=(0, 0, 0))
        u_value = i * step
        motion_path = cmds.pathAnimation(
            jnt,
            c=curve,
            fractionMode=True,
            follow=True,
            followAxis="x",
            upAxis="y",
            worldUpType="vector",
            worldUpVector=(0, 1, 0),
        )
        cmds.cutKey(motion_path, cl=True, at="u")
        cmds.setAttr(f"{motion_path}.uValue", u_value)

        jnt_pos = cmds.xform(jnt, q=True, ws=True, translation=True)
        jnt_rot = cmds.xform(jnt, q=True, ws=True, rotation=True)

        conn_nodes = get_connected_nodes(jnt)
        cmds.delete(conn_nodes)

        cmds.xform(jnt, translation=jnt_pos, ws=True)
        cmds.xform(jnt, rotation=jnt_rot, ws=True)
        
        result.append(jnt)
    
    return result



@with_selection
def align_object_to_plane(*args):
    """ Aligns the given objects to a plane defined by the first three objects.

    Notes
    -----
        **Decoration** :
            - @with_selection

    Args
    ----
        *args : str
            Minimum of 4 required.
    
    Examples
    --------
    >>> align_object_to_plane()
    >>> align_object_to_plane("joint1", "joint2", "joint3", "joint4", ...)
    ['joint4']
    """
    if len(args) < 4:
        cmds.warning("At least 4 objects are required.")
        return []


    parent_map = {}
    for obj in args:
        if not cmds.objExists(obj):
            cmds.warning(f"Object '{obj}' does not exist. Skipping.")
            continue
        
        parent = cmds.listRelatives(obj, parent=True, fullPath=False)
        parent_map[obj] = parent
        if parent:
            cmds.parent(obj, world=True)


    moved_objects = []
    try:
        p1 = om2.MVector(*cmds.xform(args[0], q=True, ws=True, t=True))
        p2 = om2.MVector(*cmds.xform(args[1], q=True, ws=True, t=True))
        p3 = om2.MVector(*cmds.xform(args[2], q=True, ws=True, t=True))

        v1 = p2 - p1
        v2 = p3 - p1
        normal = v1 ^ v2

        if normal.length() == 0:
            cmds.warning("The first three objects must not be colinear.")
            return []
        normal.normalize()

        for obj in args[3:]:
            pos = om2.MVector(*cmds.xform(obj, q=True, ws=True, t=True))
            vec = pos - p1
            distance = normal * vec
            projected = pos - normal * distance
            cmds.xform(obj, ws=True, t=(projected.x, projected.y, projected.z))
            moved_objects.append(obj)

    finally:
        for obj, parent in parent_map.items():
            if parent:
                cmds.parent(obj, parent)

    return moved_objects



@alias(n="curve_name", d="degree", cl="closed_curve")
def create_curve_from_points(
    *points: List[Tuple[float, float, float]], 
    curve_name: str = "", 
    degree: int = 1, 
    closed_curve: bool = False
) -> str:
    """ If the start and end points are the same, it creates a closed curve.

    Notes
    -----
        **Decoration** :
            - @alias(n="curve_name", d="degree", cl="closed_curve")    

    Args
    ----
        *points : tuple
            - (0, 1, 2), (3, 4, 5), (6, 7, 8), ...
        curve_name : str
        degree : int
        closed_curve: bool

    Returns
    -------
        curve name : str

    Examples
    --------
    >>> points = get_position(cmds.ls(sl=True))
    >>> create_curve_from_points(*points, cn="curve_name", d=3)
    >>> create_curve_from_points((0, 1, 2), (3, 4, 5), ..., d=1, cl=True)
    "curve1"
    """
    if not closed_curve:
        result = cmds.curve(p=points, d=degree, n=curve_name)
    else:
        points += points[:1]
        if degree == 1:
            result = cmds.curve(p=points, d=degree, n=curve_name)
        else:
            result = cmds.circle(nr=(0,1,0), s=len(points)-1, n=curve_name)
            result = result[0]
            for idx, pos in enumerate(points[:-1]):
                x, y, z = pos
                cmds.move(x, y, z, f"{result}.cv[{idx}]", ws=True)

    return result



@with_selection
def create_curve_aim(
    start_obj_or_vtx: str,
    end_obj_or_vtx: str,
    world_up_object: str = ""
) -> str:
    """ This function creates a curve connecting a start and an end. It can take objects or vertices as arguments.

    Notes
    -----
        **Decoration** :
            - @with_selection   

    Args
    ----
        start_obj_or_vtx : str
        end_obj_or_vtx : str
        world_up_object : str

    Returns
    -------
        curve name : str

    Examples
    --------
    >>> create_curve_aim() # @with_selection
    >>> create_curve_aim("pCube1", "pCube2")
    >>> create_curve_aim("pCube1", "pCube2", "locator1")
    >>> create_curve_aim("pCube1.vtx[0]", "pCube2.vtx[3]", "locator1")
    "curve1"
    """
    start = get_position(start_obj_or_vtx)[0]
    end = get_position(end_obj_or_vtx)[0]
    len = get_distance(start, end)
    if len <= 1e-8:
        raise ValueError("Start and End are the same (length 0).")

    cuv = cmds.curve(p=[(0, 0, 0), (len, 0, 0)], d=1)
    cmds.xform(cuv, ws=True, t=start)

    end_loc = cmds.spaceLocator()[0]
    cmds.xform(end_loc, ws=True, t=end)

    if world_up_object:
        up_pos = get_position(world_up_object)[0]
        up_loc = cmds.spaceLocator()[0]
        cmds.xform(up_loc, ws=True, t=up_pos)
        aim_constraint = cmds.aimConstraint(
            end_loc, 
            cuv,
            aimVector=(1, 0, 0),
            upVector=(0, 1, 0),
            worldUpType="object",
            worldUpObject=up_loc
        )[0]
        cmds.delete(aim_constraint, up_loc)
    else:
        aim_constraint = cmds.aimConstraint(
            end_loc, 
            cuv,
            aimVector=(1, 0, 0),
            upVector=(0, 1, 0),
            worldUpType="vector",
            worldUpVector=(0, 1, 0)
        )[0]
        cmds.delete(aim_constraint)

    cmds.delete(end_loc)
    cmds.rebuildCurve(cuv, d=3, s=3, rpo=1, ch=0, end=1, kr=0, kt=0)
    cmds.delete(cuv, ch=True)

    return cuv



def create_curve_animation():
    pass



def create_group_for_rig(group_name: str) -> list:
    """ This function creates a group for the rig.

    Notes
    -----
        **No Decoration** :

    Args
    ----
        group_name : str

    Returns
    -------
        created_group : str
            ["group_name", "rig", "MODEL", "controllers", "skeletons", "geoForBind", "extraNodes", "bindBones", "rigBones"]

    Examples
    --------
    >>> create_group_for_rig("butterflyA")
    ['butterflyA', 'rig', 'MODEL', 'controllers', 'skeletons', 'geoForBind', 'extraNodes', 'bindBones', 'rigBones']
    """
    if not group_name:
        return []
    
    names_of_all_groups = {
        group_name: ["rig", "MODEL"], 
        "rig": ["controllers", "skeletons", "geoForBind", "extraNodes"], 
        "skeletons": ["bindBones", "rigBones"]
    }

    result = [
        group_name, 
        "rig", 
        "MODEL", 
        "controllers", 
        "skeletons", 
        "geoForBind", 
        "extraNodes", 
        "bindBones", 
        "rigBones"
    ]

    for parents, children in names_of_all_groups.items():
        if not cmds.objExists(parents):
            cmds.group(em=True, n=parents)
        for child in children:
            if not cmds.objExists(child):
                cmds.group(em=True, n=child)
            cmds.parent(child, parents)

    return result



@with_selection
def get_parents_children(*args) -> Dict[str, List]:
    """ This function creates metadata about its parents and children.

    Notes
    -----
        **Decoration** :
            - @with_selection

    Args
    ----
        *args : str

    Returns
    -------
        meta_data : dict
            - {"item": "parents", ["child_1", "child_2"], ...}

    Examples
    --------
    >>> get_parents_children("joint2")
    {'joint2': ['joint1', ['joint3', 'joint4']]}
    """
    result = {}
    for i in args:
        is_parents = cmds.listRelatives(i, parent=True, f=False) or []
        i_parents = is_parents[0] if is_parents else ""

        is_children = cmds.listRelatives(i, children=True, f=False) or []
        i_children = is_children if is_children else []

        result[i] = [i_parents, i_children]

    return result



def extract_range_path(start: str, end: str) -> Dict[str, List]:
    """ This function separates the range structure from a complex hierarchy.

    Notes
    -----
        **No Decoration** :

    Args
    ----
        start : str
        end : str

    Returns
    -------
        meta_data : dict

    Examples
    --------
    >>> meta_data = extract_range_path("joint2", "joint15")
    >>> orient_joint("joint2")
    >>> restore_range_path(meta_data)
    """
    meta_data = get_parents_children(start)
    get_path = get_range_path(start, end)
    for i in get_path:
        parents, children = get_parents_children(i)[i]
        if parents:
            cmds.parent(i, w=True)

        extra_children = [ch for ch in children if ch not in get_path]
        if extra_children:
            temp = get_parents_children(*extra_children)
            meta_data.update(temp)
        for j in extra_children:
            cmds.parent(j, w=True)

    parent_in_sequence(*get_path)

    return meta_data



def restore_range_path(meta_data: Dict[str, List]) -> None:
    """ This function restores the hierarchy based on meta_data information.

    Notes
    -----
        **No Decoration** :

    Args
    ----
        meta_data : dict

    Examples
    --------
    >>> meta_data = extract_range_path("joint2", "joint15")
    >>> orient_joint("joint2")
    >>> restore_range_path(meta_data)
    """
    for item, parents_children in meta_data.items():
        item_parents = parents_children[0]
        if item_parents:
            cmds.parent(item, item_parents)



def split_numbers(text: str) -> Dict[int, str]:
    """ This function splits numbers and letters.

    Notes
    -----
        **No Decoration**

    Args
    ----
        text : str
            - 'vhcl_car123_rig_v0123'
            - "a0123_v2345"

    Examples
    --------
    >>> split_numbers('vhcl_car123_rig_v0123')
    {0: 'vhcl_car', 1: '123', 2: '_rig_v', 3: '0123'}
    """
    split_text = re.split(r'(\d+)', text)
    remove_blank = [i for i in split_text if i]
    result = {idx: name for idx, name in enumerate(remove_blank)}

    return result



@alias(p="prefix", s="suffix")
@with_selection
def add_affixes(*args, prefix: str = "", suffix: str = "") -> list:
    """ Add a prefix and/or suffix to each input string.

    Notes
    -----
        **Decoration**
            - @alias(p="prefix", s="suffix")
            - @with_selection

    Args
    ----
        - args : str
        - prefix : str, optional 
        - suffix : str, optional 

    Examples
    --------
    >>> add_affixes("item1", "item2", prefix="pre_", suffix="_ctrl")
    ['pre_item1_ctrl', 'pre_item2_ctrl']
    """
    result = []
    for input_string in args:
        if prefix and suffix:
            result_string = f"{prefix}{input_string}{suffix}"
        elif prefix and not suffix:
            result_string = f"{prefix}{input_string}"
        elif not prefix and suffix:
            result_string = f"{input_string}{suffix}"
        else:
            result_string = f"{input_string}"
        result.append(result_string)

    return result



@alias(n="name", p="prefix", s="suffix")
@with_selection
def re_name(*args, name: str="", prefix: str="", suffix: str=""):
    """ This function changes a name. 
    
    - Duplicate names are allowed. 
    - You can add a ``prefix`` and ``suffix`` to a name. 
    - Rename in the order you select.
    - Process in the reverse order of selection.

    Notes
    -----
        **Decoration**
            - @alias(n="name", p="prefix", s="suffix")
            - @with_selection

    Args
    ----
        - args(str) : Base name
        - name(str) : Name to change
        - prefix : str, optional
        - suffix : str, optional 

    Examples
    --------
    >>> re_name(n="tail_1", p="rig_", s="_FK")
    >>> re_name(p="rig_", s="_FK")
    >>> re_name("joint1", "joint2", n="tail_1", p="rig_", s="_FK")
    ['rig_tail_1_FK', 'rig_tail_2_FK', ...]
    """
    name_slice = split_numbers(name)
    number_only = {k: v for k, v in name_slice.items() if v.isdigit()}
    number_idx = max(number_only.keys()) if number_only else None


    org_name = {}
    new_name = []
    for idx, org in enumerate(args):
        name_slice_copy = name_slice.copy()
        if number_idx:
            num = name_slice_copy[number_idx]
            name_slice_copy[number_idx] = f"%0{len(num)}d" % (int(num)+idx)
            new = "".join(name_slice_copy.values())
        else:
            new = name + "%s" % idx if name else org.split("|")[-1]
        org_name[org] = cmds.ls(org, long=True)[0]
        new_name.append(new)


    org_name_copy = list(org_name.values()).copy()
    org_name_copy.sort(key=lambda x: x.count('|'), reverse=True)
    new_name_affix = add_affixes(*new_name, p=prefix, s=suffix)


    result = {}
    for org in org_name_copy:
        org_idx = list(org_name.values()).index(org)
        new = new_name_affix[org_idx]
        final_name = cmds.rename(org, new)
        result[org] = final_name


    reorder = []
    for arg in args:
        arg_long = org_name[arg]
        reorder.append(result[arg_long])

    return reorder



@alias(s="search", r="replace_name")
@with_selection
def replace_name(*args, search: str, replace_name: str):
    """ This function replaces ``search`` with ``replace_name``.

    Notes
    -----
        **Decoration**
            - @alias(s="search", r="replace_name")
            - @with_selection

    Args
    ----
        - args(str) : Base name
        - search : str
        - replace_name : str

    Examples
    --------
    >>> replace_name(s="FK", r="IK")
    ['rig_spine_1_IK', 'rig_spine_2_IK', ...]

    """
    org_name = {}
    new_name = []
    for org in args:
        org_long = cmds.ls(org, long=True)[0]
        org_long_end = org_long.split("|")[-1]
        new = org_long_end.replace(search, replace_name)
        org_name[org] = org_long
        new_name.append(new)


    org_name_copy = list(org_name.values()).copy()
    org_name_copy.sort(key=lambda x: x.count('|'), reverse=True)
    

    result = {}
    for org in org_name_copy:
        org_idx = list(org_name.values()).index(org)
        new = new_name[org_idx]
        final_name = cmds.rename(org, new)
        result[org] = final_name


    reorder = []
    for arg in args:
        arg_long = org_name[arg]
        reorder.append(result[arg_long])

    return reorder



@alias(obj="object", grp="group", con="constraint", loc="locator", 
       jnt="joint", clt="cluster", cuv="nurbsCurve", ikh="ikhandle")
@with_selection
def select_only(*args, **kwargs) -> list:
    """ Select objects that match one or more specified filter types.

    Notes
    -----
        **Decoration**
            - @alias(obj="object", grp="group", con="constraint", loc="locator", jnt="joint", clt="cluster", cuv="nurbsCurve", ikh="ikhandle")
            - @with_selection

    Args
    ----
        *args: str 

        **kwargs : dict
            - joint
            - ikhandle
            - constraint
            - group
            - object (mesh/nurbsSurface)
            - cluster
            - locator
            - nurbsCurve

    Examples
    --------
    >>> select_only(joint=True)
    >>> select_only(jnt=True, loc=True)
    >>> select_only('obj1', 'obj2', group=True, constraint=True)
    """
    filters = {
        "joint": kwargs.get("joint", False),
        "ikhandle": kwargs.get("ikhandle", False),
        "constraint": kwargs.get("constraint", False),
        "group": kwargs.get("group", False),
        "object": kwargs.get("object", False),
        "cluster": kwargs.get("cluster", False),
        "locator": kwargs.get("locator", False),
        "nurbsCurve": kwargs.get("nurbsCurve", False),
    }
    if not any(filters.values()):
        raise ValueError("At least one filter must be set to True.")


    result = set()

    if filters["object"]:
        shapes = cmds.ls(args, dag=True, type=['mesh', 'nurbsSurface'])
        result.update(i.getParent() for i in shapes)
    if filters["nurbsCurve"]:
        curves = cmds.ls(args, dag=True, type=['nurbsCurve'])
        result.update(i.getParent() for i in curves)


    if args: 
        sel = cmds.ls(args, dag=True, typ="transform") 
    else:
        sel = cmds.ls(sl=True, dag=True, typ="transform")


    for obj in sel:
        obj_type = cmds.objectType(obj)
        shapes = cmds.listRelatives(obj, s=True)
        node_type = cmds.nodeType(shapes[0]) if shapes else None
    
        if filters["joint"] and obj_type == "joint":
            result.add(obj)
        if filters["ikhandle"] and obj_type == "ikHandle":
            result.add(obj)
        if filters["constraint"] and "Constraint" in obj_type and not shapes:
            result.add(obj)
        if filters["group"]:
            is_constraint = "Constraint" in obj_type
            is_special = obj_type in ['joint', 'ikEffector', 'ikHandle']
            if not (shapes or is_constraint or is_special):
                result.add(obj)
        if filters["cluster"] and node_type == "clusterHandle":
            result.add(obj)
        if filters["locator"] and node_type == "locator":
            result.add(obj)
    
    cmds.select(result)

    return list(result)



def get_deformed_shape(obj: str) -> tuple:
    """ Returns the original shape (including namespace) and the shape resulting from the deformer (without namespace or intermediate) from the transform node.

    Notes
    -----
        **No Decoration**

    Args
    ----
        obj(str) : "char_tigerA_mdl_v9999:tigerA_body"
            
    Examples
    --------
    >>> get_deformed_shape("pSphere1")
    ('pSphereShape1Orig', 'pSphereShape1Deformed')
    """
    shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
    original_shape = None
    deformed_shape = None

    for shp in shapes:
        if cmds.getAttr(f"{shp}.intermediateObject"):
            original_shape = shp
        else:
            deformed_shape = shp

    return original_shape, deformed_shape



def get_MFnObject(node: str) -> Union[om2.MFnMesh, om2.MFnNurbsCurve]:
    """ Return a suitable MFn object for a given mesh or nurbsCurve node.

    Notes
    -----
        **No Decoration**

    Args
    ----
        node : str
        
    Returns
    -------
        ``om2.MFnMesh`` or ``om2.MFnNurbsCurve``

    Examples
    --------
    >>> get_MFnObject("pCube1")
    <OpenMaya.MFnMesh object at 0x00000274AC86B0F0>
    """
    shape = None
    if cmds.nodeType(node) == "transform":
        shapes = cmds.listRelatives(node, shapes=True, noIntermediate=True)
        if not shapes:
            raise ValueError(f"No shape under transform: {node}")
        shape = shapes[-1]
    else:
        shape = node


    shape_type = cmds.nodeType(shape)
    sel = om2.MSelectionList()
    sel.add(shape)
    dag_path = sel.getDagPath(0)


    if shape_type == "mesh":
        return om2.MFnMesh(dag_path)
    elif shape_type == "nurbsCurve":
        return om2.MFnNurbsCurve(dag_path)
    else:
        raise ValueError(f"{shape} is not mesh or nurbsCurve!: {shape_type})")



def get_closest_point_on_mesh(mesh: str, pos: Union[List, Tuple]) -> tuple:
    """ Compute the closest point on a mesh surface from a 
    given world-space position.

    Notes
    -----
        **No Decoration**

    Args
    ----
        mesh : str
        position : Union[List, Tuple]

    Examples
    --------
    >>> get_closest_point_on_mesh("pSphere1", (1, 2, 3))
    (0.254104, 0.566114, 0.782051)
    """
    mfn_mesh = get_MFnObject(mesh)
    world_pos = om2.MPoint(pos)
    closest_point, _ = mfn_mesh.getClosestPoint(world_pos, om2.MSpace.kWorld)

    result = om2.MVector(closest_point)

    return result



@with_selection
def get_uv_coordinates(vtx_edge_face: Union[str, object]) -> tuple:
    """ Get the (average) UV coordinates for a mesh component using OM2.

    Notes
    -----
        **Decoration**
            - @with_selection

    Args
    ----
        vtx_edge_face(str) : "pCube1.vtx[0]", "pCube1.e[3]", "pCube1.f[12]"

    Examples
    --------
    >>> get_uv_coordinates("pCube1.vtx[0]")
    (0.125, 0.375)
    >>> get_uv_coordinates("pCube1.e[10]")
    (0.51234, 0.23112)
    >>> get_uv_coordinates("pCube1.f[2]")
    (0.33333, 0.66667)
    """
    comp_str = str(vtx_edge_face).strip()
    if not comp_str or "." not in comp_str:
        om2.MGlobal.displayWarning("Mesh component like 'pCube1.vtx[0]'.")
        return ()


    sel = om2.MSelectionList()
    try:
        sel.add(comp_str)
    except Exception:
        om2.MGlobal.displayWarning("Invalid component: %s" % comp_str)
        return ()


    dag, comp = sel.getComponent(0)
    if dag.node().hasFn(om2.MFn.kTransform):
        try:
            dag.extendToShape()
        except Exception:
            om2.MGlobal.displayWarning("Could not resolve mesh shape.")
            return ()


    fn = om2.MFnMesh(dag)


    try:
        uv_set = fn.currentUVSetName()
    except Exception:
        uv_sets = fn.getUVSetNames()
        if not uv_sets:
            om2.MGlobal.displayWarning("Mesh has no UV sets.")
            return ()
        uv_set = uv_sets[0]


    uvs: list[Tuple[float, float]] = []
    api_t = comp.apiType()


    if api_t == om2.MFn.kMeshVertComponent:
        v_it = om2.MItMeshVertex(dag, comp)
        if v_it.isDone():
            return ()
        v_id = v_it.index()
        face_ids = list(v_it.getConnectedFaces() or [])
        if not face_ids:
            om2.MGlobal.displayWarning("Vertex has no connected faces.")
            return ()
        poly_it = om2.MItMeshPolygon(dag)
        first_uv = None
        for f_id in face_ids:
            try:
                poly_it.setIndex(f_id)
            except Exception:
                continue
            verts = list(poly_it.getVertices() or [])
            try:
                local_idx = verts.index(v_id)
            except ValueError:
                continue
            try:
                u, v = poly_it.getUV(local_idx, uv_set)
                first_uv = (float(u), float(v))
                break  # match PyMEL's getUV() behavior: first found
            except Exception:
                continue
        if first_uv is None:
            om2.MGlobal.displayWarning("No UVset for the given vertex.")
            return ()
        
        return round(first_uv[0], 5), round(first_uv[1], 5)


    elif api_t == om2.MFn.kMeshEdgeComponent:
        e_it = om2.MItMeshEdge(dag, comp)
        if e_it.isDone():
            return ()
        v0 = e_it.vertexId(0)
        v1 = e_it.vertexId(1)
        face_ids = list(e_it.getConnectedFaces() or [])
        poly_it = om2.MItMeshPolygon(dag)
        for f_id in face_ids:
            try:
                poly_it.setIndex(f_id)
            except Exception:
                continue
            verts = list(poly_it.getVertices() or [])
            for v_id in (v0, v1):
                try:
                    local_idx = verts.index(v_id)
                except ValueError:
                    continue
                try:
                    u, v = poly_it.getUV(local_idx, uv_set)
                    uvs.append((float(u), float(v)))
                except Exception:
                    continue
        if not uvs:
            om2.MGlobal.displayWarning("No UVs for the given edge.")
            return ()


    elif api_t == om2.MFn.kMeshPolygonComponent:
        poly_it = om2.MItMeshPolygon(dag, comp)
        if poly_it.isDone():
            return ()
        vtx_count = poly_it.polygonVertexCount()
        for i in range(vtx_count):
            try:
                u, v = poly_it.getUV(i, uv_set)
                uvs.append((float(u), float(v)))
            except Exception:
                continue
        if not uvs:
            om2.MGlobal.displayWarning("No UVs for the given face.")
            return ()


    else:
        om2.MGlobal.displayWarning("Args must be a mesh vertex/edge/face.")
        return ()


    avg_u = sum(u for u, _ in uvs) / len(uvs)
    avg_v = sum(v for _, v in uvs) / len(uvs)

    return round(avg_u, 5), round(avg_v, 5)



def get_uv_coordinates_closet_object(
    obj_closet_mesh: str, 
    mesh: str, 
    uv_set: str = "map1"
) -> Tuple[float, float]:
    """ Get UV coordinates from the closest point on a mesh to an object.

    Notes
    -----
        **No Decoration**

    Args
    ----
        obj_closet_mesh : str
        mesh : str
        uv_set : str, optional

    Examples
    --------
    >>> get_uv_coordinates_closet_object("locator1", "pSphere1")
    (0.123, 0.414)
    """
    obj_pos = cmds.xform(obj_closet_mesh, q=True, ws=True, t=True)
    world_pos = om2.MPoint(*obj_pos)
    mfn_mesh = get_MFnObject(mesh)
    closet_point, _ = mfn_mesh.getClosestPoint(world_pos, om2.MSpace.kWorld)

    u, v, _= mfn_mesh.getUVAtPoint(closet_point, om2.MSpace.kWorld, uv_set)

    return u, v



def create_follicle(mesh: str, UVCoordinates: tuple) -> str:
    """ Create ``follicles`` on mesh at the positions of ``UVCoordinates``.

    Notes
    -----
        **No Decoration**

    Args
    ----
        mesh : str
        UVCoordinates : tuple

    Examples
    --------
    >>> create_follicle("tigerA", (0.8, 0.8))
    "follicle1"
    """
    deformed_shape = get_deformed_shape(mesh)[-1]
    follicle_shape = cmds.createNode("follicle")
    follicle_node = cmds.listRelatives(follicle_shape, parent=True)[0]

    cmds.connectAttr(
        f"{follicle_shape}.outTranslate", 
        f"{follicle_node}.translate", 
        f=True
    )
    cmds.connectAttr(
        f"{follicle_shape}.outRotate", 
        f"{follicle_node}.rotate", 
        f=True
    )
    cmds.connectAttr(
        f"{deformed_shape}.outMesh", 
        f"{follicle_shape}.inputMesh", 
        f=True
    )
    cmds.connectAttr(
        f"{mesh}.worldMatrix[0]", 
        f"{follicle_shape}.inputWorldMatrix", 
        f=True
    )
    u, v = UVCoordinates
    cmds.setAttr(f"{follicle_shape}.parameterU", u)
    cmds.setAttr(f"{follicle_shape}.parameterV", v)

    return follicle_node



@alias(rx="rangeX", ry="rangeY", rz="rangeZ")
def create_setRange_node(
    node_attr: str, 
    rangeX: list=[0, 0, 0, 0], 
    rangeY: list=[0, 0, 0, 0], 
    rangeZ: list=[0, 0, 0, 0], 
) -> list:
    """ Create and configure a setRange node connected to a controller's attribute.

    Notes
    -----
        **Decoration**
            - @alias(rx="rangeX", ry="rangeY", rz="rangeZ")

    Args
    ----
        node_attr : str
        rangeX(list) : [old_min, old_max, min, max]
        rangeY(list) : [old_min, old_max, min, max]
        rangeZ(list) : [old_min, old_max, min, max]

    Examples
    --------
    >>> create_setRange_node("ctrl.IK0_FK1", rx=[0, 10, 0, 1])
    ['setRange1.outValueX', 'setRange1.outValueY', 'setRange1.outValueZ']
    """
    inputs = ['valueX', 'valueY', 'valueZ']
    outputs = ['outValueX', 'outValueY', 'outValueZ']
    range_attrs = {
        'X': ["oldMinX", "oldMaxX", "minX", "maxX"],
        'Y': ["oldMinY", "oldMaxY", "minY", "maxY"],
        'Z': ["oldMinZ", "oldMaxZ", "minZ", "maxZ"]
    }
    ranges = {
        'X': rangeX,
        'Y': rangeY,
        'Z': rangeZ
    }

    setRange_node = cmds.shadingNode("setRange", au=True)
    for i in inputs:
        cmds.connectAttr(f"{node_attr}", f"{setRange_node}.{i}", f=True)
    for axis, attrs in range_attrs.items():
        for attr, num in zip(attrs, ranges[axis]):
            cmds.setAttr(f"{setRange_node}.{attr}", num)

    result = ["%s.%s" % (setRange_node, out) for out in outputs]

    return result



@alias(t="translate", r="rotate", s="sclae")
def create_blendColor_node(
    node_attr: str, 
    fk_joint: str, 
    ik_joint: str,
    translate: bool=False, 
    rotate: bool=False, 
    scale: bool=False, 
) -> list:
    """ Create blendColors nodes to blend attributes between two joints.

    Notes
    -----
        **Decoration**
            - @alias(t="translate", r="rotate", s="sclae")

    Args
    ----
        node_attr : str
        fk_joint : str
        ik_joint : str
        translate : bool
        rotate : bool
        scale : bool
        visibility : bool

    Examples
    --------
    >>> node_attr = "cc_arm_L.IK0_FK1"
    >>> outputs = create_setRange_node(node_attr, rx=[0, 10, 0, 1])
    outputs = ['setRange1.outValueX', 'setRange1.outValueY', ...]
    >>> fk = "rig_arm_L_FK"
    >>> ik = "rig_arm_L_IK"
    >>> create_blendColor_node(outputs[0], fk, ik, t=True, r=True)
    ['blendColors1.output', 'blendColors2.output', ...]
    """
    attrs = {
        "translate": translate,
        "rotate": rotate,
        "scale": scale,
    }
    blend_attrs = [key for key, value in attrs.items() if value]

    result = []
    for attr in blend_attrs:
        blend_node = cmds.shadingNode("blendColors", au=True)
        cmds.connectAttr(
            node_attr, f"{blend_node}.blender", force=True)
        cmds.connectAttr(
            f"{fk_joint}.{attr}", f"{blend_node}.color1", force=True)
        cmds.connectAttr(
            f"{ik_joint}.{attr}", f"{blend_node}.color2", force=True)
        result.append(f"{blend_node}.output")

    return result



@alias(tc="target_ctrl", an="attr_name", k="keyable", 
       ft="float_type", bt="bool_type", et="enum_type", it="integer_type")
def create_attributes(
    target_ctrl: str,
    attr_name: str,
    keyable: bool = True,
    float_type: dict = None,
    bool_type: dict = None,
    enum_type: dict = None,
    integer_type: dict = None,
) -> dict:
    """ Creates attributes on a given controller.

    Notes
    -----
        **Decoration**
            - @alias(tc="target_ctrl", an="attr_name", k="keyable", ft="float_type", bt="bool_type", et="enum_type", it="integer_type")

    Args
    ----
        target_ctrl : str
        attr_name : str
        keyable : bool
        float_type : dict
        bool_type : dict
        enum_type : dict
        integer_type : dict

    Examples
    --------
    >>> ctrl_1 = "nurbsCircle1"
    >>> ctrl_2 = "nurbsCircle2"
    >>> attr = "IK0_FK1"
    ...
    >>> ft_dict = {"at": "double", "dv": 0, "min": 0, "max": 10}
    >>> ft_dict = {"at": "double", "dv": 0}
    >>> bt_dict = {"at": "bool"}
    >>> et_dict = {"at": "enum", "enumName": "World:Hips:Chest"}
    >>> it_dict = {"at": "long", "dv": 0}
    ...
    >>> create_attributes(ctrl_1, attr, ft=ft_dict)
    >>> create_attributes(ctrl_2, attr, bt=bt_dict)
    >>> create_attributes(ctrl_2, attr, et=et_dict)
    >>> create_attributes(ctrl_2, attr, it=it_dict)
    """
    kwargs = {
        "longName": attr_name,
        "keyable": keyable,
    }


    if float_type:
        kwargs.update(float_type)
    elif bool_type:
        kwargs.update(bool_type)
    elif enum_type:
        kwargs.update(enum_type)
    elif integer_type:
        kwargs.update(integer_type)


    if cmds.attributeQuery(attr_name, node=target_ctrl, exists=True):
        cmds.deleteAttr(f"{target_ctrl}.{attr_name}")
    cmds.addAttr(target_ctrl, **kwargs)


    return kwargs



@alias(sc="source_ctrl", tc="target_ctrl", an="attr_name", k="keyable", 
       ft="float_type", bt="bool_type", et="enum_type", it="integer_type")
def create_attributes_proxy(
    source_ctrl: str, 
    target_ctrl: str, 
    attr_name: str, 
    keyable: bool = True,
    float_type: dict = None,
    bool_type: dict = None,
    enum_type: dict = None,
    integer_type: dict = None,
) -> dict:
    kwargs = {
        "longName": attr_name,
        "keyable": keyable,
    }


    if float_type:
        kwargs.update(float_type)
    elif bool_type:
        kwargs.update(bool_type)
    elif enum_type:
        kwargs.update(enum_type)
    elif integer_type:
        kwargs.update(integer_type)


    if cmds.attributeQuery(attr_name, node=source_ctrl, ex=True):
        cmds.deleteAttr(f"{source_ctrl}.{attr_name}")
    cmds.addAttr(source_ctrl, **kwargs)


    kwargs["proxy"] = "%s.%s" % (source_ctrl, attr_name)
    if cmds.attributeQuery(attr_name, node=target_ctrl, ex=True):
        cmds.deleteAttr(f"{target_ctrl}.{attr_name}")
    cmds.addAttr(target_ctrl, **kwargs)

    return kwargs



@alias(idx="color_idx", rgb="color_rgb")
@with_selection
def colorize(*args, color_idx=None, color_rgb=()) -> None: 
    """ Applies color overrides to Maya nodes.

    Notes
    -----
        **Decoration**
            - @alias(idx="color_idx", rgb="color_rgb")
            - @with_selection

    Args
    ----
        - args : str
        - color_idx : int
        - color_rgb : tuple
    
    Color Table
    -----------
        0. gray: (0.534, 0.534, 0.534)
        1. black: (0, 0, 0)
        2. dark_gray: (0.332, 0.332, 0.332)
        3. medium_gray: (0.662, 0.662, 0.662)
        4. brick_red: (0.607, 0.258, 0.234)
        5. indigo: (0.17, 0.095, 0.44)
        6. blue: (0, 0, 1)
        7. olive_green: (0.242, 0.345, 0.184)
        8. dark_violet: (0.209, 0.096, 0.334)
        9. light_purple: (0.744, 0.33, 0.871)
        10. brown: (0.55, 0.384, 0.287)
        11. dark_brown: (0.299, 0.217, 0.189)
        12. rust: (0.595, 0.297, 0.118)
        13. red: (1, 0, 0)
        14. lime_green: (0, 1, 0)
        15. periwinkle: (0.295, 0.336, 0.645)
        16. white: (1, 1, 1)
        17. yellow: (1, 1, 0)
        18. light_cyan: (0.673, 1, 1)
        19. pale_green: (0.616, 1, 0.648)
        20. light_pink: (1, 0.78, 0.761)
        21. peach: (1, 0.76, 0.545)
        22. chartreuse: (0.840, 1, 0)
        23. forest_green: (0.443, 0.645, 0.426)
        24. tan: (0.631, 0.497, 0.291)
        25. khaki: (0.675, 0.693, 0.324)
        26. sage_green: (0.548, 0.683, 0.324)
        27. moss_green: (0.476, 0.679, 0.455)
        28. teal_blue: (0.49, 0.68, 0.695)
        29. slate_blue: (0.392, 0.469, 0.683)
        30. lavender_gray: (0.468, 0.304, 0.678)
        31. rose: (0.608, 0.333, 0.478)

    Examples
    --------
    >>> colorize("sphere1", color_idx=15) # periwinkle
    >>> colorize("sphere1", color_rgb=(0.631, 0.497, 0.291)) # tan
    >>> colorize(idx=13) # red
    >>> colorize(idx=6) # blue
    >>> colorize(idx=17) # yellow
    >>> colorize(idx=9) # light_purple
    >>> colorize(idx=18) # light_cyan
    >>> colorize(idx=20) # light_pink
    """
    def _shapes_for(node_name):
        node_name = str(node_name)
        if not cmds.objExists(node_name):
            return []
        if cmds.objectType(node_name, isAType="shape"):
            shapes = [node_name]
        else:
            shapes = cmds.listRelatives(
                node_name, shapes=True, noIntermediate=True, fullPath=True
            ) or []


        valid = []
        for s in shapes:
            if not cmds.attributeQuery("overrideEnabled", node=s, exists=True):
                continue
            if cmds.attributeQuery("intermediateObject", node=s, exists=True):
                if cmds.getAttr(f"{s}.intermediateObject"):
                    continue
            if cmds.attributeQuery("visibility", node=s, exists=True):
                if not cmds.getAttr(f"{s}.visibility"):
                    continue
            valid.append(s)

        return valid


    use_index = color_idx is not None
    use_rgb = (not use_index) and bool(color_rgb) and len(color_rgb) == 3


    if not (use_index or use_rgb):
        return


    r = g = b = None
    if use_rgb:
        r, g, b = [max(0.0, min(1.0, float(c))) for c in color_rgb]


    for arg in args:
        for shp in _shapes_for(arg):
            # Enable overrides
            cmds.setAttr(f"{shp}.overrideEnabled", 1)
            if use_index:
                cmds.setAttr(f"{shp}.overrideRGBColors", 0)
                cmds.setAttr(f"{shp}.overrideColor", int(color_idx))
            else:  # use_rgb
                cmds.setAttr(f"{shp}.overrideRGBColors", 1)
                cmds.setAttr(f"{shp}.overrideColorRGB", r, g, b)



class ColorPickerUI:
    """ A UI tool for setting the overrideColor index of selected shapes 
    in Maya using a compact and neatly padded RGB palette grid. 

    Examples
    --------
    >>> cpu = ColorPickerUI()
    >>> cpu.show()
     """
    dt = Data()
    COLOR_CHART = dt.color_chart
    WINDOW_NAME = "ColorPickerWin"


    def __init__(self):
        """ A UI tool for setting the overrideColor index of selected shapes 
        in Maya using a compact and neatly padded RGB palette grid. 

        Examples
        --------
        >>> cpu = ColorPickerUI()
        >>> cpu.show()
         """
        self.palette_items = list(self.COLOR_CHART.items())
        self.selected_idx = 0


    def select_color(self, idx, *args):
        """ Set the currently selected palette color index.

        Args:
            idx (int): The palette color index.
        """
        self.selected_idx = idx


    def apply_color(self, *args):
        """ Apply the selected color index to the overrideColor 
        of all selected shapes in Maya.
         """
        sel = cmds.ls(selection=True) or []
        if not sel:
            cmds.warning("Please select a controller.")
            return

        colorize(*sel, color_idx=self.selected_idx)
        try:
            cmds.inViewMessage(amg="Color index applied.", pos="topCenter", fade=True)
        except Exception:
            # inViewMessage may not be available in some environments; ignore gracefully
            pass


    def close(self, *args):
        """ Close the palette UI window. """
        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME)


    def show(self):
        """ Display the color palette UI with balanced padding. """
        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME)

        grid_rows = 4
        grid_cols = 8
        grid_btn_h = 20
        grid_btn_w = 26
        btn_h = 22
        side_padding = 4
        top_padding = 2
        bottom_padding = 10

        window_w = (grid_cols * grid_btn_w) + (side_padding * 2)
        window_h = (grid_rows * grid_btn_h) + (2 * btn_h)
        window_h += top_padding + bottom_padding + 18

        win = cmds.window(
            self.WINDOW_NAME,
            title="Color Picker",
            widthHeight=(window_w, window_h),
            sizeable=False
        )
        cmds.showWindow(win)
        cmds.setParent(win)
        cmds.columnLayout(adjustableColumn=True, rowSpacing=3, columnAttach=("both", side_padding))
        cmds.separator(h=top_padding, style='none')

        cmds.frameLayout(labelVisible=False, marginWidth=0, marginHeight=0, borderVisible=False)
        cmds.gridLayout(numberOfColumns=grid_cols, cellWidthHeight=(grid_btn_w, grid_btn_h))

        for idx, (name, rgb) in enumerate(self.palette_items):
            # Capture current idx with default arg to avoid late-binding in lambdas
            cmds.button(
                label="",
                backgroundColor=rgb,
                command=(lambda _=None, i=idx: self.select_color(i)),
                annotation=f"{name}: index={idx}, rgb={rgb}"
            )

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.separator(h=8, style='none')
        cmds.button(label="Apply", height=btn_h, command=self.apply_color)
        cmds.button(label="Close", height=btn_h, command=self.close)
        cmds.separator(h=10, style='none')

        cmds.setParent('..')
        cmds.setParent('..')



sel = cmds.ls(sl=True)


# pos = [get_position(i)[0] for i in sel]
# create_curve_from_points(*pos, cn="cuv_tail_guide_R_1", d=3)


# a = re_name(n="rig_tail_follicle_guide_1")
# parent_in_sequence(*a)


# mesh = "poly_tail_guide"
# for i in sel:
#     uv = get_uv_coordinates_closet_object(i, mesh)
#     create_follicle(mesh, uv)


# for p, c in zip(sel[:11], sel[11:]):
#     cmds.pointConstraint(p, c, mo=True, w=1.0)


# dt = Data()
# points = dt.ctrl_shapes["cube"]
# create_curve_from_points(*points, d=1, n="cc_wing_LF_2")


# names = re_name(n="cc_leg_RB_FK_1")
# names_grp = group_with_pivot(*sel)
# for i in range(len(names_grp)):
#     if i+1 < len(names_grp):
#         cmds.parent(names_grp[i+1][0], names_grp[i][-1])
#     if i == 0:
#         try:
#             cmds.parent(names_grp[i][0], w=True)
#         except Exception as e:
#             print(e)


# replace_name(s="_IK", r="")


# a = parent_in_sequence()
# group_with_pivot(*a)
# group_with_pivot()



# ft_dict = {"at": "double", "dv": 0, "min": 0, "max": 10}
# attr_name = "IK0_FK1"
# for i in ["LM", "LB", "RF", "RM", "RB"]:
#     cc = f"cc_foot_{i}"
#     joints = [f'rig_leg_{i}_{n}' for n in range(2, 6)]
#     fk_joints = [f'rig_leg_{i}_FK_{n}' for n in range(2, 6)]
#     ik_joints = [f'rig_leg_{i}_IK_{n}' for n in range(2, 6)]
#     create_attributes(cn=cc, an=attr_name, ft=ft_dict)
#     set_range_out = create_setRange_node(cc, attr_name, rx=[0, 10, 0, 1])
#     for jnt, fk_jnt, ik_jnt in zip(joints, fk_joints, ik_joints):
#         blend_node = create_blendColor_node(set_range_out[0], set_range_out[1], fk_jnt, ik_jnt, t=True, r=True)
#         cmds.connectAttr(f"{blend_node[0]}.{blend_node[-1]}", f"{jnt}.translate", f=True)
#         cmds.connectAttr(f"{blend_node[1]}.{blend_node[-1]}", f"{jnt}.rotate", f=True)



# ft_dict = {"at": "double", "dv": 0}
# attr_name = "Toe_Rotate_Z"
# for i in ["LF", "LM", "LB", "RF", "RM", "RB"]:
#     cc = f"cc_foot_{i}"
#     toe = f"cc_toe_{i}_grp"
#     create_attributes(cc, attr_name, ft=ft_dict)
#     cmds.connectAttr(f"{cc}.{attr_name}", f"{toe}.rotateZ", f=True)



# ft_dict = {"at": "double", "dv": 0, "min": 0, "max": 10}
# attr_name = "IK0_FK1"
# for i in ["LF", "LM", "LB", "RF", "RM", "RB"]:
#     cc1 = f"cc_leg_{i}_FK_1"
#     cc2 = f"cc_leg_{i}_FK_2"
#     create_attributes(cc1, attr_name, ft=ft_dict)
#     create_attributes(cc2, attr_name, ft=ft_dict, proxy=cc1)
#     create_attributes(cc3, attr_name, ft=ft_dict, proxy=cc2)



# ft_dict = {"at": "double", "dv": 0, "min": 0, "max": 10}
# attr_name = "IK0_FK1"
# for i in ["LF", "LM", "LB", "RF", "RM", "RB"]:
#     cc3 = f"cc_leg_{i}_FK_3"
#     create_attributes(f"cc_foot_{i}", attr_name, ft=ft_dict, proxy=cc3)



# cpu = ColorPickerUI()
# cpu.show()


# select_only(ikh=True)


# replace_name(s="rig_", r="")


# for i in sel:
#     target = "rig_" + i
#     # cmds.connectAttr(f"{target}.translate", f"{i}.translate", f=True)
#     # cmds.connectAttr(f"{target}.rotate", f"{i}.rotate", f=True)
#     cmds.disconnectAttr(f"{target}.translate", f"{i}.translate")
#     cmds.disconnectAttr(f"{target}.rotate", f"{i}.rotate")


# for i in sel:
#     grp = cmds.group(em=True)
#     cmds.parent(grp, i)
#     cmds.setAttr(f"{grp}.translateX", 0)
#     cmds.setAttr(f"{grp}.translateY", 0)
#     cmds.setAttr(f"{grp}.translateZ", 0)
#     cmds.setAttr(f"{grp}.rotateX", 0)
#     cmds.setAttr(f"{grp}.rotateY", 0)
#     cmds.setAttr(f"{grp}.rotateZ", 0)



# ft_dict = {"at": "double", "dv": 0, "min": 0, "max": 10}
# create_attributes("ctrl", "IK0_FK1", ft=ft_dict)


# node_attr = "ctrl.IK0_FK1"
# setRange_node = create_setRange_node(node_attr, rx=[0, 10, 0, 1])
# print(setRange_node)


# for jnt in ["joint2", "joint3", "joint4"]:
#     blendColor_node = create_blendColor_node(setRange_node[0], f"{jnt}_FK", f"{jnt}_IK", t=True, r=True)
#     print(blendColor_node)
#     for j, k in zip(blendColor_node, ["translate", "rotate"]):
#         cmds.connectAttr(j, f"{jnt}.{k}", f=True)



@alias(sx="scaleX", sy="scaleY", sz="scaleZ")
def create_ikSplineHandle(
    curve_name: str, 
    joints: list, 
    scaleX=False, 
    scaleY=False, 
    scaleZ=False
) -> None:
    scales = []
    if scaleX:
        scales.append("X")
    if scaleY:
        scales.append("Y")
    if scaleZ:
        scales.append("Z")

        
    curve_info = cmds.shadingNode("curveInfo", au=True)
    cmds.connectAttr(f"{curve_name}.worldSpace[0]", f"{curve_info}.inputCurve", f=True)
    curve_length = cmds.getAttr(f"{curve_info}.arcLength")
    multiplyDivide_node = cmds.shadingNode("multiplyDivide", au=True)
    cmds.setAttr(f"{multiplyDivide_node}.operation", 2)
    cmds.setAttr(f"{multiplyDivide_node}.input2X", curve_length)
    cmds.connectAttr(f"{curve_info}.arcLength", f"{multiplyDivide_node}.input1X", f=True)
    for jnt in joints:
        for scl in scales:
            cmds.connectAttr(f"{multiplyDivide_node}.outputX", f"{jnt}.scale{scl}", f=True)



# points = get_position(*sel)
# cuv = create_curve_from_points(*points, n="cuv", d=3)


@with_selection
def test(*joints, scaleX=True, scaleY=True, scaleZ=True):
    joint_points = get_position(*joints)
    curve_name = cmds.curve(d=3, editPoint=joint_points)
    curve_shape = cmds.listRelatives(curve_name, shapes=True)[0]
    cp_count = cmds.getAttr(curve_shape + ".controlPoints", size=True)
    for i in range(cp_count):
        locator = cmds.spaceLocator()
        cp_pos = get_position(f"{curve_name}.cv[{i}]")[0]
        cmds.xform(locator, translation=cp_pos, ws=True)
        locator_shape = cmds.listRelatives(locator, shapes=True)[0]
        cmds.connectAttr(f"{locator_shape}.worldPosition[0]", f"{curve_shape}.controlPoints[{i}]", f=True)

    cmds.ikHandle(
        sj=joints[0], 
        ee=joints[-1], 
        curve=curve_name, 
        sol="ikSplineSolver", 
        rootOnCurve=True, 
        createCurve=False, 
        parentCurve=False, 
    )
    
    



