from piece import Piece
from plateau import Plateau

class Game:
    def __init__(self, x:int, y:int):

    def generer_pioche(self):
        self.pioche = []

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    for l un range(2):
                        pioche += [Piece(i,j,k,l)]