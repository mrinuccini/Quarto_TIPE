from piece import Piece
from plateau import Plateau

class Game:
    def __init__(self, x=4, y=4):
        self.generer_pioche()
        self.afficher_pioche()

    def generer_pioche(self):
        "Génère la pioche du jeu"
        self.pioche = {}

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    for l in range(2):
                        self.pioche[i,j,k,l] = Piece(i,j,k,l)
    
    def afficher_pioche(self):
        print("PIOCHE ⛏️\n"+"-"*70)
        for key in self.pioche.keys():
            print(f"{key} : {self.pioche[key]}")


game = Game()