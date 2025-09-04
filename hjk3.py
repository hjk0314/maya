# -*- coding: utf-8 -*-


from typing import List, Tuple, Union
# from collections import Counter
import time
import functools
import math
# import re
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
def get_downstream_path(start_jnt: str, end_jnt: str) -> list:
    """ Get the downstream ``joints`` or ``objects`` 
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
    >>> get_downstream_path('joint2', 'joint10')
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



@with_selection
def orient_joints(*args, **kwargs) -> None:
    """ Select joints and don't put anything in the argument, 
    it will be oriented with the Maya default settings.
    
    This function orients all joints. Freeze forces all joints below it to zero rotation.
    
    Notes
    -----
        **Decoration** : @with_selection

    Args
    ----
        - *args : str
            joint1, joint2, joint3 ...
        - kwargs: 
            - Maya default: xyz, yup
            - Mixamo: yzx, zup
            - Left hand: yxz, zdown

    Examples
    --------
    >>> orient_joints(p="yzx", s="zup") # Mixamo
    >>> orient_joints(p="yxz", s="zdown") # Left hand
    >>> orient_joints(p="xyz", s="yup") # Default
    ...
    >>> orient_joints() # @with_selection
    >>> orient_joints("joint1", "joint4")
    >>> orient_joints(*["joint1", "joint2"], p="yzx", s="zup")
    """
    valid_primary = {"xyz", "yzx", "zxy", "zyx", "yxz", "xzy", "none"}
    valid_secondary = {"xup", "xdown", "yup", "ydown", "zup", "zdown", "none"}
    primary = "xyz"
    secondary = "yup"


    for k, v in kwargs.items():
        if k in ("primary", "p") and v in valid_primary:
            primary = v
        elif k in ("secondary", "s") and v in valid_secondary:
            secondary = v
        else:
            cmds.warning(f"Ignored invalid flag: {k}={v}")

    cmds.makeIdentity(args, apply=True, jointOrient=True, normal=False)

    for jnt in args:
        cmds.joint(
            jnt,
            edit=True,
            children=True,
            zeroScaleOrient=True,
            orientJoint=primary,
            secondaryAxisOrient=secondary
        )

    end_joints = []
    for j in args:
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
        if cmds.nodeType(i) == 'transform':
            node = i
        else:
            parent = cmds.listRelatives(i, parent=True, fullPath=False)
            if parent:
                node = parent[0]
            else:
                continue

        grp_name = [f"{node}_grp"]
        if kwargs.get("null", False):
            grp_name.append(f"{node}_null")


        groups = []
        for gn in grp_name:
            gn = "" if cmds.objExists(gn) else gn
            grp = cmds.group(em=True, n=gn)
            cmds.matchTransform(grp, node, pos=True, rot=True)
            groups.append(grp)
        groups.append(node)


        top_group = cmds.listRelatives(node, parent=True, fullPath=False)
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


@alias(cn="curve_name", d="degree", cl="closed_curve")
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
            - @alias(cn="curve_name", d="degree", cl="closed_curve")    

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


# a = get_bounding_box_position()
# loc = cmds.spaceLocator()
# cmds.xform(loc, t=a, ws=True)


# joints = create_joint_on_curve_path("curve2", n=6)
# jnt = parent_in_sequence(*joints)
# orient_joints(*jnt)


# create_curve_aim()


# sel = cmds.ls(sl=True, fl=True)
# pos = get_position(*sel)
# for i in pos:
#     cmds.select(cl=True)
#     jnt = cmds.joint(p=(0,0,0))
#     cmds.xform(jnt, t=i, ws=True)


# cuv = create_curve_from_points(*pos, d=1)
# joints = create_joint_on_curve_path(cuv, n=3)
# jnt = parent_in_sequence(*joints)
# orient_joints(*jnt)


# sel = cmds.ls(sl=True)
# orient_joints()


# a = get_bounding_box_position()
# cmds.select(cl=True)
# jnt = cmds.joint(p=(0,0,0))
# loc = cmds.spaceLocator()
# cmds.xform(loc, t=a, ws=True)


# b = parent_in_sequence()
orient_joints()


# orient_joints(p="yxz", s="zdown")
# group_with_pivot(null=True)

# create_pole_vector_joints()
