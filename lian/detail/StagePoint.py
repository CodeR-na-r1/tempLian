from ..Point import Point

class StagePoint:

    def __init__(self, point: Point, distance, angle, isReBind) -> None:

        self.point = point

        self.distance = distance
        self.angle = angle

        self.isReBind__ = isReBind

    def isChangeConnectivity(self):
        
        return self.isReBind__

    def __eq__(self, __value: object) -> bool:

        return self.point == __value.point# and self.distance == __value.distance

    def __hash__(self):

        # return hash(((self.x, self.y), self.distance))
        return hash((self.x, self.y))
    
    def __str__(self) -> str:

        return f"StagePoint(coord: {self.point}, distance: {self.distance}, angle: {self.angle})"