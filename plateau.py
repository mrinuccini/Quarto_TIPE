from piece import Piece, comp
from toolbox import convert_matrice

class Plateau:
    arr = []
    x = 0
    y = 0

    def __init__(self, x=4, y=4) -> None:
        """
            Créé un nouveau tableau de taille (x, y) avec toutes les pièces sans caractéristiques
        """
        assert(x > 0)
        assert(y > 0)

        self.arr = [[None for i in range(0, x)] for i in range(0, y)]
        self.x = x
        self.y = y

    def reinitialiser(self) -> None:
        for x in range(0, self.x):
            for y in range(0, self.y):
                self.arr[y][x] = None

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

    def verifier_alignements(self) -> bool:
        """
            Vérifie si le plateau contient un aligments (mais ne précise pas où se trouve cet alignement !)
        """
        # Vérification des lignes
        has_line = any(comp(self.arr[i]) for i in range (self.x))

        # Vérifications des colonnes
        columns = convert_matrice(self.arr)
        has_column = any(comp(columns[i]) for i in range(self.x))

        # Vérifiction diagonales
        diag = False

        diagonale1 = []
        diagonale2 = []
        for i in range (0, self.x):
            diagonale1.append(self.arr[i][i])
            diagonale2.append(self.arr[self.x - i - 1][self.x - i - 1])

        diag = comp(diagonale1) or comp(diagonale2)
        
        return diag or has_line or has_column

    def recuperer_cases_vides(self) -> list:
        """
            Renvoie l'ensemble des cases vides sous la forme d'une liste avec leur indice
        """
        empty = []

        for x in range(0, self.x):
            for y in range(0, self.y):
                if self.arr[y][x] == None:
                    empty.append(x + (y * self.x))

        return empty

    def __repr__(self) -> str:
        out = ""
        for y in range(0, self.y):
            for x in range(0, self.x):
                str = ""
                if self.arr[y][x] == None:
                    str += f"[#{x+y*self.x}]"
                    str += " " * (8 - len(str))
                else:
                    str += repr(self.arr[y][x])
                    str += " " * (7 - len(str))

                out += (str + " | ") 
            out += "\n"

        return out