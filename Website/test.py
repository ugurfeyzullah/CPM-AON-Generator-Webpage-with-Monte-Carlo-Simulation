"""t5 =  list(range(0, 59, 6))
print(t5)

# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
a=IN[0]
# Place your code below this line
from Autodesk.DesignScript.Geometry import *

t5 = list(range(0, 58, 6))
for i in a
point1 = Point.ByCoordinates(0, 0, i)
plane1 = Plane.ByOriginNormal(point1, Vector.ByCoordinates(0, 0, 1))
t12 = 30
t13 = 42.5
ellipse1 = Ellipse.ByPlaneRadii(plane1, t12, t13)
t7 = range(0, 9, 1)
t14 = List.GetItemAtIndex(ellipse1, t7)
t6 = range(-10, 10, 1)
geometry1 = Geometry.Rotate(t14, plane1, t6)
t9 = range(8, 26, 1)
t15 = List.GetItemAtIndex(ellipse1, t9)
t8 = range(0, 18, 3)
geometry2 = Geometry.Rotate(t15, plane1, t8)
t11 = range(24, 40, 1)
t16 = List.GetItemAtIndex(ellipse1, t11)
t10 = range(50, 17, 8)
geometry3 = Geometry.Rotate(t16, plane1, t10)
t2 = range(38, 52, 1)
t17 = List.GetItemAtIndex(ellipse1, t2)
t1 = range(159, 17, 3)
geometry4 = Geometry.Rotate(t17, plane1, t1)
t4 = range(50, 57, 1)
t18 = List.GetItemAtIndex(ellipse1, t4)
t3 = range(192, 8, 1)
geometry5 = Geometry.Rotate(t18, plane1, t3)
t19 = [geometry1, geometry2, geometry3, geometry4, geometry5]
solid1 = Solid.ByLoft(t19)
importInstance1 = ImportInstance.ByGeometry(solid1)

# Assign your output to the OUT variable.
OUT = t19"""""""""

"""t5 = list(range(0, 58, 6))
centerpoints=[]
for i in t5:
    point1 = Point.ByCoordinates(0, 0, i)
    centerpoints.append(point1)
print(centerpoints)"""

step = -10
result1 = []

for _ in range(9):
    result1.append(step)
    step += 1

print(result1)

step = 0
result2 = []

for _ in range(16):
    result2.append(step)
    step += 3

print(result2)

step = 50
result3 = []

for _ in range(14):
    result3.append(step)
    step += 8

print(result3)

step = 159
result4 = []

for _ in range(11):
    result4.append(step)
    step += 3

print(result4)

step = 192
result5 = []

for _ in range(7):
    result5.append(step)
    step += 1

print(result5)

combined_list=result1+result2+result3+result4+result5
print(combined_list)

result1 = [step + i for i in range(9) for step in [-10]]
result2 = [step + i * 3 for i in range(16) for step in [0]]
result3 = [step + i * 8 for i in range(14) for step in [50]]
result4 = [step + i * 3 for i in range(11) for step in [159]]
result5 = [step + i for i in range(7) for step in [192]]

combined_list2 = result1 + result2 + result3 + result4 + result5
print(combined_list2)

t5 = list(range(0, 57, 1))
print(t5)