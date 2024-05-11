# -*- coding: utf-8 -*-
__doc__ = 'python for revit api'
__author__ = 'NguyenThanhSon' "Email: nguyenthanhson1712@gmail.com"
import string
import importlib
ARC = string.ascii_lowercase
begin = "".join(ARC[i] for i in [13, 0, 13, 2, 4, 18])
module = importlib.import_module(str(begin))
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
from pyrevit import revit, DB, UI
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
try:
    Ele = module.get_selected_elements(uidoc,doc)
    def disallow_join_at_end(element, ind):
        Autodesk.Revit.DB.WallUtils.DisallowWallJoinAtEnd(element,ind)

    def pick_point_with_nearest_snap():       
        snap_settings = UI.Selection.ObjectSnapTypes.None
        prompt = "Click"
        try:

            click_point = uidoc.Selection.PickPoint(snap_settings, prompt)
            
        except:
            # print(traceback.format_exc())
            pass
        return click_point

    def distance_2_point(point , reference_point):
        distance = point.DistanceTo(reference_point)
        return distance

    def get_nearest_point(points, reference_point):
        min_distance = float('inf')
        nearest_point = None
        
        for point in points:
            distance = point.DistanceTo(reference_point)
            if distance < min_distance:
                min_distance = distance
                nearest_point = point
        return nearest_point

    point = pick_point_with_nearest_snap()
    gia_tri_dieu_chinh = -100
    for i in Ele:
        get_para_value_start = module.get_parameter_value_by_name(i, "Start Level Offset", is_UTF8 = False)
        get_para_value_end = module.get_parameter_value_by_name(i, "End Level Offset", is_UTF8 = False)
        curve_beam = i.Location.Curve
        start_point = curve_beam.GetEndPoint(0)
        end_point = curve_beam.GetEndPoint(1)
        tim_point = get_nearest_point([start_point,end_point], point)
        t = Transaction (doc, "Chỉnh level 1 đầu dầm")
        t.Start()
        if tim_point == start_point:
            set_para_value_start = module.set_parameter_value_by_name(i, "Start Level Offset", (float(get_para_value_start) + gia_tri_dieu_chinh)/304.8, is_UTF8 = False)
        else:
            set_para_value_end = module.set_parameter_value_by_name(i, "End Level Offset", (float(get_para_value_end) + gia_tri_dieu_chinh)/304.8, is_UTF8 = False)
        t.Commit()
except:
    pass