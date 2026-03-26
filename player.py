"Instanciation des joueurs"
TYPES = ["Humain", "Monte Carlo", "MinMax"]

from piece import *
from plateau import *

class Joueur:
    def __init__(self, typ="Humain", niveau=1):
        """ Paramètre :
                type : chaîne de caractères, élément de TYPES
                       type de joueur
                niveau : entier naturel
                         niveau de l'IA (si non humain)
        """
        assert(typ in TYPES)
        self.type = typ
        self.niveau = niveau

    def choisir_piece(self, plateau, pioche):
        """ Choix d'une pièce que devra placer le joueur suivant, selon le type du joueur """
        #Joueur humain
        if self.type == "Humain":
            cond = True
            while cond: #On ne s'arrête que quand le joueur a sélectionné une pièce valide
                i = int(input("Veuillez choisir une pièce : "))
                if i in pioche: #Si la pièce est disponible dans la pioche
                    cond = False
                else:
                    print("Pièce indisponible, veuillez réessayer !")
            return i

    def choisir_place(self, plateau, pioche, piece):
        """ Choix du placement de la pièce selon le type du joueur """
        #Joueur humain
        if self.type == "Humain":
            #Sélection de la position
            cond = True
            while cond: #On ne s'arrête que quand le joueur choisi une position valide
                i = int(input("Veuillez choisir une position où placer la pièce : "))
                row_idx = i % plateau.x
                column_idx = i // plateau.x
                if plateau.arr[column_idx][row_idx] == None:
                    cond = False
            return i