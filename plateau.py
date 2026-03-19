from piece import Piece

class Plateau:
    arr = []
    x = 0
    y = 0

    def __init__(self, x: int, y: int) -> None:
        assert(x > 0)
        assert(y > 0)

        self.arr = [[Piece(0, 0, 0, 0) for i in range(o, x)] for i in range(0, y)]
        self.x = x
        self.y = y

    def recuperer_piece(self, x:int, y: int) -> Piece:
        assert(0 <= x <= self.x)
        assert(0 <= y <= self.y)

        return arr[y, x]
