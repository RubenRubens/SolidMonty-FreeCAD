from Montys_FreeCAD import *


A = cube(1)
B = translate([6, 0, 0]) (A)
C = A + B
export_STL(C, "R")


# A = cube(1)
# B = translate([6, 0, 0]) (A)
# A = cube(1)
# C = A + B
# export_STL(C, "R")


