from ..Point import Point

class Map:

    def __init__(self, image) -> None:
        self.image = image

    @property
    def shape(self):
        return self.image.shape

    def isFree(self, point: Point):
        return self.image[point.y][point.x] != 0

    # def __eq__(self, __value: object) -> bool:
    #     return self.x == __value.x and self.y == __value.y

    # def __str__(self) -> str:
    #     return f"Point({self.x}, {self.y})"