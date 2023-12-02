class Path:

    def __init__(self, vertexes, distance: int, sumAngles: int) -> None:
        self.vertexes = vertexes
        self.distance = distance
        self.sumAngles = sumAngles

    def __eq__(self, __value: object) -> bool:
        return self.distance == __value.distance and self.sumAngles == __value.sumAngles

    def __hash__(self):
        return hash((self.vertexes, (self.distance, self.sumAngles)))

    # TODO sum angles for next operations

    def __lt__(self, __value) -> bool:  #  implement operator <
        return self.distance < __value.distance

    def __gt__(self, __value) -> bool:  #  implement operator >
        return self.distance > __value.distance

    def __str__(self) -> str:
        return f"Path(vertexes: {self.vertexes}, distance: {self.distance})"