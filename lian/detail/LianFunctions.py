from typing import Dict, List

from time import sleep

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from ..Point import Point
from .StagePoint import StagePoint
from .Map import Map

from .Geometry import midpoint, distanceBetweenPoints, angleBetweenVectors, lineOfSight

def validPath(points: Point, map: Map) -> bool:

    for point in points:
        if not map.isFree(point):
            return False
        
    return True

def Expand(currentPoint: StagePoint, distanceDelta: int, end: StagePoint, angleDelta: int, mapPath: Dict[Point, Point], mapDistances: Dict[Point, int], mapAngles: Dict[Point, int], CLOSE: List[StagePoint], map: Map):

    points = midpoint(currentPoint.point, distanceDelta)

    open = []
    
    for point in points:

        if point.x < 0 or point.x >= map.shape[1] or point.y < 0 or point.y >= map.shape[0]:
            continue
        if not map.isFree(point):
            continue
        angle = 0
        if currentPoint.point in mapPath and mapPath[currentPoint.point] != None:   # можно вынести за цикл и проверять один раз, а сюда подставлять флаг
            angle = angleBetweenVectors(mapPath[currentPoint.point], currentPoint.point, currentPoint.point, point)
            if angle > angleDelta:
                continue
        if not validPath(lineOfSight(currentPoint.point, point, distanceDelta), map):
            continue

        stagePoint = StagePoint(point, currentPoint.distance + distanceBetweenPoints(currentPoint.point, point), mapAngles[currentPoint.point] + angle, False) # ? parent Point or StagePoint

        if stagePoint in CLOSE:
            if stagePoint.distance < mapDistances[point]:

                print("MATCH!")
                mapPath[point] = currentPoint.point

                mapDistances[point] = stagePoint.distance
                mapAngles[point] = stagePoint.angle

                stagePoint.isReBind__ = True
                open.append(stagePoint) # ? (возможно нужно обновить пути дочерних, если они лучше, то те тоже попадцт и обновят свои расстояния)

            continue
        # if stagePoint in CLOSE: # !DANG place 1
        #     continue

        if (point not in mapAngles
            or (point in mapAngles and stagePoint.angle < mapAngles[point])
            or (point in mapDistances and stagePoint.distance < mapDistances[point])):
            
            if point not in mapAngles:
                open.append(stagePoint)
            else:
                stagePoint.isReBind__ = True
                print("INVARIANT BAD FAILURE")
                exit(-1)

            mapPath[point] = currentPoint.point

            mapDistances[point] = stagePoint.distance
            mapAngles[point] = stagePoint.angle

            open.append(stagePoint)

    if distanceBetweenPoints(currentPoint.point, end.point) < distanceDelta and end not in open:

        pEnd = StagePoint(end.point,
                               currentPoint.distance + distanceBetweenPoints(currentPoint.point, end.point),
                               mapAngles[currentPoint.point] + angleBetweenVectors(mapPath[currentPoint.point], currentPoint.point, currentPoint.point, end.point), False)
        
        mapPath[pEnd.point] = currentPoint.point

        mapDistances[pEnd.point] = pEnd.distance
        mapAngles[pEnd.point] = pEnd.angle

        open.append(pEnd)

    return open

def unwindingPath(mapPath: Dict[Point, Point], start: Point, end: Point) -> List[Point]:

    path = [end]
    
    current = end
    while mapPath[current] != None and current != start:
        
        current = mapPath[current]

        path.append(current)
    
    path.reverse()

    return path

def saveImage(nameFile: str, image):
    cv.imwrite(nameFile, image)

def drawImage(map: Map, OPEN: List[StagePoint], CLOSE: List[StagePoint], path: List[Point], points: List[Point], mapPath: Dict[Point, Point]):

    THICKNESS = 3

    image = map.image.copy()
    image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    
    for closePoint in CLOSE:
        image = cv.circle(image, (closePoint.point.x, closePoint.point.y), THICKNESS, (141, 174, 240), 1)
    for openPoint in OPEN:
        image = cv.circle(image, (openPoint.point.x, openPoint.point.y), THICKNESS, (160,32,240), 1)

    for pathPoint in path:
        image = cv.circle(image, (pathPoint.x, pathPoint.y), THICKNESS * 2, (33, 0, 38), 1)
    
    if len(mapPath) > 0 and len(points) == 2:
        currentPath = unwindingPath(mapPath=mapPath, start=points[0], end=points[1])
        for pathPoint in currentPath:
            image = cv.circle(image, (pathPoint.x, pathPoint.y), THICKNESS, (255, 0, 0), 1)

    return image

def showImage(image):

    imgSize = (800, 600)
    image = cv.resize(src=image, dsize=imgSize)
    cv.imshow("Lian processing...", image)
    k = cv.waitKey(1)

# function for thread
def showImageThread(flagAction: List[bool], map: Map, OPEN: List[StagePoint], CLOSE: List[StagePoint], path: List[Point], points: List[Point], mapPath: Dict[Point, Point]):

    while (flagAction[0]):

        image = drawImage(map, OPEN, CLOSE, path, points, mapPath)

        showImage(image=image)

        sleep(0.2)

    print("thread finished")