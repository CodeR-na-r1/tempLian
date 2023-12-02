# main file for start Lian algorithm

# imports

from typing import List
import numpy as np

import time, datetime

from threading import Thread

from .Point import Point
from .detail.StagePoint import StagePoint
from .detail.Path import Path
from .detail.Map import Map

from .detail.LianFunctions import unwindingPath, Expand, drawImage, showImage, showImageThread, saveImage
from .detail.Geometry import distanceBetweenPoints

# debug data

__DEBUG = True

def __Log(msg):
    if __DEBUG:
        print("__Log: " + msg)

# lian implementation

def LIAN(start: Point, end: Point, distanceDelta: int, angleDelta: int, image: np.ndarray, pathSnapshotsOfSolutions: str = None) -> List[Point]:
    
    timer = time.time()

    MAX_INT = image.shape[0] * image.shape[1]

    OPEN = []   # queue of vertexes (type -> StagePoint)
    CLOSE = []  # list of visited vertexes (type -> StagePoint)

    start = StagePoint(start, 0, 0, False)
    end = StagePoint(end, MAX_INT, MAX_INT, False)
    OPEN.append(start)

    mapPath = {}    # value is parent for key (type -> Point)
    mapPath[start.point] = None

    mapDistances = {}   # value is distance for key (type -> Point)
    mapDistances[start.point] = 0

    mapAngles = {}   # value is sum angles for key (type -> Point)
    mapAngles[start.point] = 0

    map = Map(image=image)

    bestPath = Path([], MAX_INT, MAX_INT)

    pathHit = 0
    iterCounter = 0

    threadFlagAction = [True]
    threadPoints = [start.point, start.point]   # start, end
    thread = Thread(target=showImageThread, args=(threadFlagAction, map, OPEN, CLOSE, bestPath.vertexes, threadPoints, mapPath))
    thread.start()

    __Log(f"Lian started...")
    
    while len(OPEN) > 0:
        
        # currentPoint = sorted(OPEN, key=lambda x: x.distance + distanceBetweenPoints(p1=x.point, p2=end.point))[0]
        # if len(bestPath.vertexes) == 0:
            # print("one")
            # currentPoint = min(OPEN, key=lambda x: distanceBetweenPoints(p1=x.point, p2=end.point))
        # else:
            # print("two")
        lpoints = filter(lambda x: x.isReBind__ == True, OPEN)

        if len(list(lpoints)) > 0:
            currentPoint = lpoints[0]
            print("ReBind")
        else:
            currentPoint = min(OPEN, key=lambda x: x.distance + distanceBetweenPoints(p1=x.point, p2=end.point))
            print("NO rebind")

        OPEN.remove(currentPoint)

        if currentPoint.point == end.point:

            pathHit += 1
            __Log(f"find -> {pathHit}")

            print(mapDistances[end.point])
            print(bestPath.distance)
            if mapDistances[end.point] < bestPath.distance: # change on angles and also for exPAnd()
                # Каждый новый путь будет все сглаженнее и сглаженнее - инвариант функции Expand, поэтому здесь True
               
                __Log("Path unwinding...")
                path = unwindingPath(mapPath, start.point, end.point)
                bestPath = Path(path, mapDistances[end.point], mapAngles[end.point])
                __Log("Path found!")
                if pathSnapshotsOfSolutions != None:    # save image of path
                    image = drawImage(map, [], [], path, [], {})
                    saveImage(pathSnapshotsOfSolutions + f"Path_{pathHit}.png", image)
                    with open(pathSnapshotsOfSolutions + f"path_{pathHit}.txt", 'w') as f:
                        f.write("Path Search Parameters:\n")
                        f.write(f"Distance delta -> {distanceDelta}px\n")
                        f.write(f"Angle delta -> {angleDelta}°\n{'-' * 15}\n")
                        f.write("Path characteristics:\n")
                        f.write(f"Distance -> {bestPath.distance}px\n")
                        f.write(f"Sum angles -> {bestPath.sumAngles}°\n{'-' * 15}\n")
                        f.write(f"Pathfinding time -> {str(datetime.timedelta(seconds=time.time() - timer))}\n{'-' * 15}\n")
                        f.write("Points of path:\n")
                        for point in path:
                            f.write(str(point) +  f" Angle = {mapAngles[point]}" + "\n")
                        f.write(f"{'-' * 15}")
                    __Log("Path saved!")
        else:
            if currentPoint not in CLOSE:
                CLOSE.append(currentPoint)
            # Настройка алгоритма: Если не устроил путь, то увеличить коэффициент в этом условии
            if (currentPoint.distance + distanceBetweenPoints(p1=currentPoint.point, p2=end.point) > bestPath.distance * 1.015
            or currentPoint.angle > bestPath.sumAngles): # Оптимизация -> Если дистанция до финиша через эту точку больше протяженности лучшего пути на 5%, то отрбасываем ее + условие с углом
                print("Skip")
                continue    # Если даже по прямой путь дальше текущего найденного пути, то отбрасываем точку
            else:

                openExtend = Expand(currentPoint, distanceDelta, end, angleDelta, mapPath, mapDistances, mapAngles, CLOSE, map)
                for point in openExtend:
                    if point in OPEN:
                        OPEN.remove(point)
                    OPEN.append(point)

        threadPoints[1] = currentPoint.point

        __Log(f"Iteration -> {iterCounter}")
        iterCounter += 1

    threadFlagAction[0] = False
    thread.join()

    __Log(f"Lian finished...")
    __Log(f"Total number of iterations -> {iterCounter}")
    __Log(f"Total number of paths found -> {pathHit}")

    return bestPath.vertexes