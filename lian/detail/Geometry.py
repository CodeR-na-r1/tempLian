# functions for operations with geometry

import math

from typing import List

from ..Point import Point

def distanceBetweenPoints(p1: Point, p2: Point) -> float:
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

def angleBetweenVectors(a1: Point, a2: Point, b1: Point, b2: Point) -> float:

    ax = a2.x - a1.x
    ay = a2.y - a1.y
    bx = b2.x - b1.x
    by = b2.y - b1.y

    angle = math.atan2(by, bx) - math.atan2(ay, ax)

    return abs(angle *180 /math.pi)

# def angleBetweenVectors(a1: Point, a2: Point, b1: Point, b2: Point) -> float:

#     ax = a2.x - a1.x
#     ay = a2.y - a1.y 
#     bx = b2.x - b1.x
#     by = b2.y - b1.y
#     ab = ax * bx + ay * by
#     a = distanceBetweenPoints(a1, a2)
#     b = distanceBetweenPoints(b1, b2)
#     if a * b == 0:
#         return 360
#     else:
#         cos = round(ab / (a * b), 5)
#         return math.acos(cos) * 180 / math.pi

# def lineOfSight(a: Point, b: Point) -> List[Point]:

#     dx = b.x - a.x
#     dy = b.y - a.y

#     d = dy - (dx/2)
#     x = a.x
#     y = a.y

#     points = []

#     points.append(Point(x, y))
    
#     while (x < b.x): 
        
#         x=x+1
        
#         if(d < 0): 
#             d = d + dy  

#         else: 
#             d = d + (dy - dx)  
#             y=y+1

#         points.append(Point(x, y))
        
#     return points

def lineOfSight(p1, p2, nb_points=8) -> List[Point]:

    x_spacing = (p2.x - p1.x) / (nb_points + 1)
    y_spacing = (p2.y - p1.y) / (nb_points + 1)

    return [Point(int(p1.x + i * x_spacing), int(p1.y +  i * y_spacing))
            for i in range(1, nb_points+1)]

def midpoint(point: Point, r: int) -> List[Point]:

    points = []
    x_centre = point.x
    y_centre = point.y

    x = r
    y = 0
    points.append(Point(x + x_centre, y + y_centre))
    if r > 0:
        points.append(Point(-x + x_centre, -y + y_centre))
        points.append(Point(y + x_centre, x + y_centre))
        points.append(Point(-y + x_centre, -x + y_centre))
	
    P = 1 - r 

    while x > y:
	
        y += 1
        if P <= 0: 
            P = P + 2 * y + 1
			
        else:		 
            x -= 1
            P = P + 2 * y - 2 * x + 1
		
        if (x < y):
            break
		
        points.append(Point(x + x_centre, y + y_centre))
        points.append(Point(-x + x_centre, y + y_centre))
        points.append(Point(x + x_centre, -y + y_centre))
        points.append(Point(-x + x_centre, -y + y_centre))
		
        if x != y:
            points.append(Point(y + x_centre, x + y_centre))
            points.append(Point(-y + x_centre, x + y_centre))
            points.append(Point(y + x_centre, -x + y_centre))
            points.append(Point(-y + x_centre, -x + y_centre))

    return points