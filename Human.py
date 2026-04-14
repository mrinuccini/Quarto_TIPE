from piece import *
from plateau import *
from Algo import Algorithm

class Joueur(Algorithm):
    """
        Algorithme humain
    """

    def choisir_piece(self, plateau, pioche):
        cond = True
        while cond: #On ne s'arrête que quand le joueur a sélectionné une pièce valide
            i = int(input("Veuillez choisir une pièce : "))
            if i in pioche: #Si la pièce est disponible dans la pioche
                cond = False
            else:
                print("Pièce indisponible, veuillez réessayer !")
        return i

    def choisir_place(self, plateau, pioche, piece):
        #Sélection de la position
        cond = True
        while cond: #On ne s'arrête que quand le joueur choisi une position valide
            i = int(input("Veuillez choisir une position où placer la pièce : "))
            row_idx = i % plateau.x
            column_idx = i // plateau.x
            if plateau.arr[column_idx][row_idx] == None:
                cond = False
        return i