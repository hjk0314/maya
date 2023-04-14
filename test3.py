# -*- coding: utf-8 -*-

"""
Can call it here for now then it should be from global shotgun_modules
"""
import sys
sys.path.append("W:/System/Pipeline/MMU/mmu_venv/lib/site-packages/")
from sg_python_api import shotgun_api3
sg = shotgun_api3.Shotgun("https://madmanpost.shotgunstudio.com", login="kiran", password="Kiran@123")


def get_all_projects():
    """

    :return:
    """
    fields = ['name', 'id', 'sg_status']
    filters = []
    data = sg.find('Project', filters, fields)

    return data


print(get_all_projects())