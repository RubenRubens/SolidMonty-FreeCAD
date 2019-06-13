import FreeCAD, Part, Mesh, Draft
from FreeCAD import Base
import math
import Montys_FreeCAD_encapsulated_code as Encap




# FreeCAD Document Creation

FreeCAD.newDocument('test')
FreeCAD.setActiveDocument('test')
FreeCAD.ActiveDocument = FreeCAD.getDocument('test')




# 3D objects parent class

class parts:
    def __init__(self, object_id):
        self.identifier = object_id

    def __add__(self, other):
        return union(self, other)

    def __sub__(self, other):
        return difference(self, other)

    def __mul__(self, other):
        return intersection(self, other)




# 3D primitives

class cube(parts):
    '''
    Creates a cube of size = [lenght, wide, height]. By default it is not centered.
    size can be just a number to set equal the dimensions.
    '''
    def __init__(self, size=1, center=False):
        if isinstance(size, (float, int)):
            size = [size, size, size]
        self.identifier = "Part" + str(Encap.part_counter())
        new_object = FreeCAD.ActiveDocument.addObject("Part::Feature", self.identifier)
        if center == False:
            new_object.Shape = Part.makeBox(size[0], size[1], size[2])
        else:
            new_object.Shape = Part.makeBox(size[0], size[1], size[2], Base.Vector(-size[0]*0.5, -size[1]*0.5, -size[2]*0.5))


class sphere(parts):
    '''
    Creates a sphere of radius r at the origin.
    '''
    def __init__(self, r = 1, d = None):
        if d != None:
            r = d / 2
        self.identifier = "Part" + str(Encap.part_counter())
        new_object = FreeCAD.ActiveDocument.addObject("Part::Feature", self.identifier)
        new_object.Shape = Part.makeSphere(r)


class cylinder(parts):
    '''
    Creates a cylinder of radius r and height h. It's center can be placed at the origin.
    '''
    def __init__(self, r = 1, h = 1, center = False):
        self.identifier = "Part" + str(Encap.part_counter())
        new_object = FreeCAD.ActiveDocument.addObject("Part::Feature", self.identifier)
        if center == False:
            new_object.Shape = Part.makeCylinder(r, h)
        else:
            new_object.Shape = Part.makeCylinder(r, h, Base.Vector(0, 0, -h*0.5))


class cone(parts):
    '''
    Creates a cone given a height and two radius. If the second of the radius is omited it
    is set to 0. It's center can be placed at the origin.
    '''
    def __init__(self, h = 1, r1 = 1, r2 = 0, center = False):
        self.identifier = "Part" + str(Encap.part_counter())
        new_object = FreeCAD.ActiveDocument.addObject("Part::Feature", self.identifier)
        if center == False:
            new_object.Shape = Part.makeCone(r1, r2, h)
        else:
            new_object.Shape = Part.makeCone(r1, r2, h, Base.Vector(0, 0, -h*0.5))




# 2D primitives

class circle:
    def __init__(self,  r, d=None):
        if d != None:
            r = d * 0.5
        self.identifier = 'Skectch' + str(Encap.sketch_counter())
        new_object = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObject', self.identifier)
        new_object.addGeometry(Part.Circle(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), r))


def arc(center, start_point, end_point, clockwise=False):
    if clockwise == True:
        (start_point, end_point) = (end_point, start_point)
    alpha = math.atan2(start_point[1], start_point[0])
    beta = math.atan2(end_point[1], end_point[0])
    if alpha < beta:
        omega = (alpha + beta) * 0.5
    else:
        omega = (alpha + beta) * 0.5 + math.pi
    if (start_point[0] - center[0]) ** 2 + (start_point[1] - center[1]) ** 2 == (end_point[0] - center[0]) ** 2 + (end_point[1] - center[1]) ** 2:
        R = ((start_point[0] - center[0]) ** 2 + (start_point[1] - center[1]) ** 2) ** 0.5
    else:
        raise Exception('The 3 points do not form an arc.')
    middle_point = [R * math.cos(omega), R * math.sin(omega)]
    
    # Points are overwriten as FreeCAD objects
    start_point = Base.Vector(start_point[0], start_point[1], 0)
    end_point = Base.Vector(end_point[0], end_point[1], 0)
    middle_point = Base.Vector(middle_point[0], middle_point[1], 0)
    return Part.Arc(start_point, middle_point, end_point)


class line:
    def __init__(self, start_point, end_point):
        self.identifier = 'Skectch' + str(Encap.sketch_counter())
        new_object = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObject', self.identifier)
        start_point = Base.Vector(start_point[0], start_point[1], start_point[2])
        end_point = Base.Vector(end_point[0], end_point[1], end_point[2])
        new_object.addGeometry(Part.LineSegment(start_point, end_point))
        FreeCAD.ActiveDocument.recompute()


class polyline:
    def __init__(self, points, closed=True):
        self.identifier = 'Skectch' + str(Encap.sketch_counter())
        new_object = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObject', self.identifier)
        for i in range(len(points) - 1):
            start_point = Base.Vector(points[0 + i][0], points[0 + i][1], 0)
            end_point = Base.Vector(points[1 + i][0], points[1 + i][1], 0)
            new_object.addGeometry(Part.LineSegment(start_point, end_point))
        if closed:
            start_point = Base.Vector(points[0][0], points[0][1], 0)
            end_point = Base.Vector(points[len(points) - 1][0], points[len(points) - 1][1], 0)
            new_object.addGeometry(Part.LineSegment(start_point, end_point))
        FreeCAD.ActiveDocument.recompute()


class spline:
    def __init__(self, points, closed = True, rounded = False):
        if closed:
            if rounded:
                C = True
            else:
                points.append(points[0])
                C = False
        else:
            C = False

        self.identifier = 'Sketch' + str(Encap.sketch_counter())
        FreeCAD.ActiveDocument.addObject('Sketcher::SketchObject', self.identifier)
        List = []
        for point in points:
            List.append(FreeCAD.Vector(point[0], point[1], 0))
        FreeCAD.ActiveDocument.getObject(self.identifier).addGeometry(Part.BSplineCurve(List, None, None, C, 3, None, False), False)
        FreeCAD.ActiveDocument.recompute()




# Creating 3D objects from 2D primitives

def extrude(h=1):
    def inner(f):
        sketch_identifier = f.identifier
        part_identifier = 'Part' + str(Encap.part_counter())
        new_object = FreeCAD.ActiveDocument.addObject("Part::Extrusion", part_identifier)
        new_object.Base = FreeCAD.ActiveDocument.getObject(sketch_identifier)
        new_object.DirMode = "Normal"
        new_object.DirLink = None
        new_object.LengthFwd = h
        new_object.LengthRev = 0
        new_object.Solid = True
        new_object.Reversed = False
        new_object.Symmetric = False
        new_object.TaperAngle = 0
        new_object.TaperAngleRev = 0
        FreeCAD.ActiveDocument.recompute()
        return parts(part_identifier)
    return inner


def revolve(axis,  angle=360):
    if axis == 'X':
        axis = [1, 0, 0]
    elif axis == 'Y':
        axis = [0, 1, 1]
    elif axis == 'Z':
        axis == [0, 0, 1]

    def inner(f):
        sketch_identifier = f.identifier
        part_identifier = 'Part' + str(Encap.part_counter())
        new_object = FreeCAD.ActiveDocument.addObject("Part::Revolution", part_identifier)
        new_object.Source = FreeCAD.ActiveDocument.getObject(sketch_identifier)
        new_object.Axis = (axis[0], axis[1], axis[2])
        new_object.Base = (0, 0, 0)
        new_object.Angle = angle
        new_object.Solid = False
        FreeCAD.ActiveDocument.recompute()
        return parts(part_identifier)
    return inner


class loft(parts):
    def __init__(self, sections):
        self.identifier = 'Part' + str(Encap.part_counter())
        new_object = FreeCAD.ActiveDocument.addObject('Part::Loft', self.identifier)
        List = []
        for section in sections:
            List.append(FreeCAD.ActiveDocument.getObject(section.identifier))
        new_object.Sections = List
        new_object.Solid = True
        new_object.Ruled = False
        new_object.Closed = False
        FreeCAD.ActiveDocument.recompute()


class sweep(parts):
    def __init__(self, sketch, path):
        self.identifier = 'Part' + str(Encap.part_counter())
        new_object = FreeCAD.ActiveDocument.addObject('Part::Sweep', self.identifier)
        new_object.Sections = [FreeCAD.ActiveDocument.getObject(sketch.identifier)]
        new_object.Spine = FreeCAD.ActiveDocument.getObject(path.identifier)
        new_object.Solid = True
        new_object.Frenet = False
        FreeCAD.ActiveDocument.recompute()




# Rotation and Translation

def translate(vector):
    def inner(f):
        object_name = f.identifier
        FreeCAD.ActiveDocument.getObject(object_name).Placement.Base.x = vector[0]
        FreeCAD.ActiveDocument.getObject(object_name).Placement.Base.y = vector[1]
        FreeCAD.ActiveDocument.getObject(object_name).Placement.Base.z = vector[2]
        FreeCAD.ActiveDocument.recompute()
        return parts(object_name)
    return inner


def rotate(axis, angle=None, axis_pos = [0, 0, 0]):
    if axis == 'X':
        axis = [1, 0, 0]
    elif axis == 'Y':
        axis = [0, 1, 1]
    elif axis == 'Z':
        axis == [0, 0, 1]

    def inner(f):
        object_name = f.identifier
        if angle == None:
            pass
        else:
            FreeCAD.ActiveDocument.getObject(object_name).Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,0), FreeCAD.Rotation(FreeCAD.Vector(axis[0], axis[1], axis[2]), angle), FreeCAD.Vector(axis_pos[0], axis_pos[1], axis_pos[2]))
            FreeCAD.ActiveDocument.recompute()
        return parts(object_name)
    return inner




# Boolean operations

class union(parts):
    '''
    Creates a new solid out of the union of two objects.
    '''
    def __init__(self, obj1, obj2):
        self.identifier = "Boolean" + str(Encap.boolean_counter())
        new_object = FreeCAD.ActiveDocument.addObject("Part::Fuse", self.identifier)
        new_object.Base = FreeCAD.ActiveDocument.getObject(obj1.identifier)
        new_object.Tool = FreeCAD.ActiveDocument.getObject(obj2.identifier)
        FreeCAD.ActiveDocument.recompute()


class intersection(parts):
    '''
    Performs the intersection of two solids.
    '''
    def __init__(self, obj1, obj2):
        self.identifier = "Boolean" + str(Encap.boolean_counter())
        new_object = FreeCAD.ActiveDocument.addObject("Part::Common", self.identifier)
        new_object.Base = FreeCAD.ActiveDocument.getObject(obj1.identifier)
        new_object.Tool = FreeCAD.ActiveDocument.getObject(obj2.identifier)
        FreeCAD.ActiveDocument.recompute()


class difference(parts):
    '''
    The first object is the one to cut and the second is the cutting tool.
    '''
    def __init__(self, obj1, obj2):
        self.identifier = "Boolean" + str(Encap.boolean_counter())
        new_object = FreeCAD.ActiveDocument.addObject("Part::Cut", self.identifier)
        new_object.Base = FreeCAD.ActiveDocument.getObject(obj1.identifier)
        new_object.Tool = FreeCAD.ActiveDocument.getObject(obj2.identifier)
        FreeCAD.ActiveDocument.recompute()




# Export the geometry to a CAD file

def export_STL(objects, name = "X"):
    '''
    Exports a STL file of an object (or a list of objects) to the current working directory.
    name sets the STL file name.
    '''
    if isinstance(objects, (list, tuple)):
        objs = []
        for obj in objects:
            objs.append(FreeCAD.getDocument("test").getObject(obj.identifier))
    else:
        objs = [FreeCAD.getDocument("test").getObject(objects.identifier)]
    Mesh.export(objs, name + ".stl")


def export_IGES(objects, name = "X"):
    if isinstance(objects, (list, tuple)):
        objs = []
        for obj in objects:
            objs.append(FreeCAD.getDocument("test").getObject(obj.identifier))
    else:
        objs = [FreeCAD.getDocument("test").getObject(objects.identifier)]
    Part.export(objs, name + ".igs")


def export_STEP(objects, name = "X"):
    if isinstance(objects, (list, tuple)):
        objs = []
        for obj in objects:
            objs.append(FreeCAD.getDocument("test").getObject(obj.identifier))
    else:
        objs = [FreeCAD.getDocument("test").getObject(objects.identifier)]
    Part.export(objs, name + ".step")


def export_SVG(objects, name = "X"): # Does not work.
    import importSVG

    if isinstance(objects, (list, tuple)):
        objs = []
        for obj in objects:
            objs.append(FreeCAD.getDocument("test").getObject(obj.identifier))
    else:
        objs = [FreeCAD.getDocument("test").getObject(objects.identifier)]
    importSVG.export(objs, name + ".svg")




# Save the FreeCAD Document

def save_FreeCAD(name):
    FreeCAD.getDocument('test').saveAs(name + '.fcstd')

