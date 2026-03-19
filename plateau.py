from piece import Piece

class Plateau:
    arr = []
    x = 0
    y = 0

    def __init__(self, x: int, y: int) -> None:
        """
            Créé un nouveau tableau de taille (x, y) avec toutes les pièces sans caractéristiques
        """
        assert(x > 0)
        assert(y > 0)

        self.arr = [[None for i in range(0, x)] for i in range(0, y)]
        self.x = x
        self.y = y

    def recuperer_piece(self, x:int, y: int) -> Piece:
        """
            Récupère la pièce à la position (x, y)
        """
        assert(0 <= x < self.x)
        assert(0 <= y < self.y)

        return self.arr[y][x]

    def placer_piece(self, x: int, y: int, piece: Piece) -> None:
        """
            Permet de placer une pièce à la position (x, y) sur le plateau
        """
        assert(0 <= x < self.x)
        assert(0 <= y < self.y)

        if self.arr[y][x] != None:
            print(f"Impossible de placer une pièce à la position (x={x}; y={y}).")
            return

        self.arr[y][x] = piece

    def __repr__(self) -> str:
        out = ""
        for y in range(0, self.y):
            for x in range(0, self.x):
                out += repr(self.arr[y][x])
                out += " | "
            out += "\n"

        return out