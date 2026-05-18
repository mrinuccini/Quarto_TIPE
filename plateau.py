from piece import *
from toolbox import *
import copy

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
        self.chemins = self.generer_chemins()
        self.x = x
        self.y = y

    def cloner(self):
        """
            Renvoie un clone du plateau actuel
        """
        clone = Plateau(x=self.x, y=self.y)
        clone.arr = [[self.arr[y][x] for x in range(0, self.x)] for y in range(0, self.y)]
        return clone

    def reinitialiser(self) -> None:
        for x in range(0, self.x):
            for y in range(0, self.y):
                self.arr[y][x] = None


    def recuperer_piece_1D(self, id: int) -> Piece:
        """
            Récupère la pièce associée à la coordonée id en une dimension
        """
        return self.recuperer_piece(id % self.x, id // self.x)

    def recuperer_piece(self, x:int, y: int) -> Piece:
        """ Récupère la pièce à la position (x, y) """
        assert(0 <= x < self.x)
        assert(0 <= y < self.y)

        return self.arr[y][x]

    def placer_piece(self, x: int, y: int, piece: Piece) -> None:
        """ Permet de placer une pièce à la position (x, y) sur le plateau """
        assert(0 <= x < self.x)
        assert(0 <= y < self.y)

        if self.arr[y][x] != None and piece != None:
            print(f"Impossible de placer une pièce à la position (x={x}; y={y}).")
            return

        self.arr[y][x] = piece

    def placer_piece_1D(self, id: int, piece: Piece) -> None:
        """ Place la pièce à la coordonée id en une dimension """
        return self.placer_piece(id % self.x, id // self.x, piece)

    def generer_chemins(self):
        chemins = []
        for y in range(0, 4): chemins.append([(x, y) for x in range(4)]) # Lignes
        for x in range(0, 4): chemins.append([(x, y) for y in range(4)]) # Colonnes

        # Diagonales
        chemins.append([(0, 0), (1, 1), (2, 2), (3, 3)])
        chemins.append([(0, 3), (1, 2), (2, 1), (3, 0)])

        return chemins


    def recuperer_lignes_diagonales(self) -> list:
        """ Renvoie une liste contenant les quatres lignes, quatres colonnes et deux diagonales """
        # lignes
        out = [self.arr[0], self.arr[1], self.arr[2], self.arr[3]]

        # Colonnes
        out.extend([
            [self.arr[0][0], self.arr[1][0], self.arr[2][0], self.arr[3][0]],
            [self.arr[0][1], self.arr[1][1], self.arr[2][1], self.arr[3][1]], 
            [self.arr[0][2], self.arr[1][2], self.arr[2][2], self.arr[3][2]],
            [self.arr[0][3], self.arr[1][3], self.arr[2][3], self.arr[3][3]]
        ])

        # Diagonales
        out.append([self.arr[0][0], self.arr[1][1], self.arr[2][2], self.arr[3][3]]) 
        out.append([self.arr[3][0], self.arr[2][1], self.arr[1][2], self.arr[0][3]])

        return out

    def verifier_alignements(self) -> bool:
        """ Vérifie si le plateau contient un aligments (mais ne précise pas où se trouve cet alignement !) """
        for chemin in self.chemins:
            if self.arr[chemin[0][1]][chemin[0][0]] is None or \
                self.arr[chemin[1][1]][chemin[1][0]] is None or \
                self.arr[chemin[2][1]][chemin[2][0]] is None or \
                self.arr[chemin[3][1]][chemin[3][0]] is None:
                continue

            p1 = self.arr[chemin[0][1]][chemin[0][0]]
            p2 = self.arr[chemin[1][1]][chemin[1][0]]
            p3 = self.arr[chemin[2][1]][chemin[2][0]]
            p4 = self.arr[chemin[3][1]][chemin[3][0]]

            if (p1.couleur == p2.couleur == p3.couleur == p4.couleur) or \
                (p1.forme == p2.forme == p3.forme == p4.forme) or \
                (p1.dessus == p2.dessus == p3.dessus == p4.dessus) or \
                (p1.taille == p2.taille == p3.taille == p4.taille):
                return True

        return False

    def recuperer_cases_vides(self) -> list:
        """ Renvoie l'ensemble des cases vides sous la forme d'une liste avec leur indice """
        return [(x+(y*self.x)) for x in range(self.x) for y in range(self.y) if self.arr[y][x] == None]

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
    

class Move:
    "Coup lors d'un tour"
    def __init__(self, place:int, piece_idx:int):
        """ Paramètres :
                place : int, position où on va placer la pièce en cours
                piece_idx : int, indice de la pièce à donner à l'adversaire
        """
        self.place = place
        self.piece_idx = piece_idx

    def get_place(self):
        "Renvoie où placer la pièce"
        return self.place
    
    def get_piece_idx(self):
        "Renvoie l'indice de la pièce à jouer pour l'autre joueur"
        return self.piece_idx #test

class RootState:
    "État de jeu (en début du tour) = plateau + pioche + une pièce à placer"
    def __init__(self, plateau:Plateau, pioche:dict, piece_a_jouer:Piece):
        self.plateau = plateau
        self.pioche = copy.deepcopy(pioche)
        self.piece_a_jouer = piece_a_jouer

    def cloner(self):
        "Renvoie un clone de l'état de jeu"
        return RootState(self.plateau.cloner(), copy.deepcopy(self.pioche), self.piece_a_jouer)
    
    def appliquer(self, move):
        self.plateau.placer
        pass