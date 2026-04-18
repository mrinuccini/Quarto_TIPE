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

    def cloner(self) -> Plateau:
        """
            Renvoie un clone du plateau actuel
        """
        clone = Plateau(x=self.x, y=self.y)
        clone.arr = [[self.arr[y][x] for x in range(0, self.x)] for y in range(0, y)]

        return clone

    def reinitialiser(self) -> None:
        for x in range(0, self.x):
            for y in range(0, self.y):
                self.arr[y][x] = None


    def recuperer_piece_1D(self, id: int) -> Piece:
        """
            Récupère la pièce associée à la coordonée id en une dimension
        """
        return recuperer_piece(id % self.x, id // self.x)

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

    def placer_piece_1D(self, id: int, piece: Piece) -> None:
        """
            Place la pièce à la coordonée id en une dimension
        """
        return placer_piece(id % self.x, id // self.x, piece)

    def recuperer_lignes_diagonales(self) -> list:
        """
            Renvoie une liste contenant les quatres lignes, quatres colonnes et deux diagonales
        """
        out = [line for line in self.arr] # Lignes

        for column in convert_matrice(self.arr): # Colonnes
            out.append(column)

        diagonale1 = []
        diagonale2 = []
        for i in range (0, self.x):
            diagonale1.append(self.arr[i][i])
            diagonale2.append(self.arr[self.x - i - 1][self.x - i - 1])

        out.append(diagonale1)
        out.append(diagonale2)

        return out

    def verifier_alignements(self) -> bool:
        """
            Vérifie si le plateau contient un aligments (mais ne précise pas où se trouve cet alignement !)
        """
        lignes_colonnes_diagonales = self.recuperer_lignes_diagonales()
        return any(comp(self.arr[i]) for i in range (self.x))

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