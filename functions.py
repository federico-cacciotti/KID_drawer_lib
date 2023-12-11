import numpy as np
import ezdxf
from ezdxf.addons import Importer
from shapely.geometry import Polygon
from pathlib import Path
import os

# returns a rectangle from opposite corners coordinates as a Polygon
def draw_rectangle_corner_dimensions(corner0, x_size, y_size):
    points =    (corner0,
                (corner0[0]+x_size, corner0[1]),
                (corner0[0]+x_size, corner0[1]+y_size),
                (corner0[0], corner0[1]+y_size))
    return Polygon(points)

# returns a rectangle from opposite corners coordinates as a lwpolyline
def draw_rectangle_corner_dimensions_points(corner0, x_size, y_size):
    points =    (corner0,
                (corner0[0]+x_size, corner0[1]),
                (corner0[0]+x_size, corner0[1]+y_size),
                (corner0[0], corner0[1]+y_size))
    return points

# adds a rectangle from the center coordinates and dimensions as a lwpolyline
def draw_rectangle_center_dimensions(center, x_size, y_size):
    points =   ((center[0]-0.5*x_size, center[1]-0.5*y_size),
                (center[0]+0.5*x_size, center[1]-0.5*y_size),
                (center[0]+0.5*x_size, center[1]+0.5*y_size),
                (center[0]-0.5*x_size, center[1]+0.5*y_size))
    return Polygon(points)



def add_feedlineSegment(pixel, fl_width, separation, fl_length=None):
    
    KID_width = x_offset = pixel.capacitor_finger_width*np.ceil(pixel.capacitor_finger_number) + pixel.capacitor_finger_gap*np.ceil(pixel.capacitor_finger_number-1.0) + pixel.absorber_separation + pixel.vertical_size
    
    x_midpoint = 0.5*pixel.vertical_size - 0.5*KID_width
    y0 = 0.5*pixel.vertical_size + pixel.coupling_capacitor_y_offset + pixel.coupling_capacitor_width + separation
    
    if fl_length == None:
        fl_length = x_midpoint+0.5*pixel.vertical_size + 0.2*pixel.vertical_size
        
    x0 = x_midpoint -0.5*fl_length
    
    points = ((x0, y0), 
              (x0+fl_length, y0), 
              (x0+fl_length, y0+fl_width),
              (x0, y0+fl_width))
    pixel.msp.add_lwpolyline(points, close=True, dxfattribs={"layer": 'FEEDLINE'})


def draw_circularWafer(wafer_diameter, metallisable_area_diameter, filename):
    # Create a new DXF R2018 drawing
    dxf = ezdxf.new('R2018', setup=True)
    # layer names
    wafer_layer_name = "WAFER"
    metallisable_area_layer_name = "METALLISABLE_AREA"
    
    # layer colors
    wafer_layer_color = 1
    metallisable_area_color = 3
    
    # adds layers
    dxf.layers.add(name=wafer_layer_name, color=wafer_layer_color)
    dxf.layers.add(name=metallisable_area_layer_name, color=metallisable_area_color)
    
    # adds a modelspace
    msp = dxf.modelspace()
    
    # drawing
    msp.add_circle((0.0, 0.0), radius=0.5*wafer_diameter, dxfattribs={"layer": wafer_layer_name})
    msp.add_circle((0.0, 0.0), radius=0.5*metallisable_area_diameter, dxfattribs={"layer": metallisable_area_layer_name})
    
    # make dxf directory
    filename = Path(filename)
    if not os.path.exists(filename.parent):
        os.makedirs(filename.parent)

    dxf.saveas(filename)
    
    
