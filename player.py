"Instanciation des joueurs"

#Importations
from minmax import *
from montecarlo import *
import random
import time

TYPES = ["Humain", "MonteCarlo", "MinMax", "RandomBot"]

class Joueur:
    def __init__(self, typ="Humain", niveau=1, param={}):
        """ Paramètre :
                type : chaîne de caractères, élément de TYPES
                       type de joueur
                niveau : entier naturel
                         niveau de l'IA (si non humain)
        """
        assert(typ in TYPES)
        self.type = typ
        self.niveau = niveau

        if self.type == "MinMax":
            self.max_depth = param["max_depth"]
        if self.type == "MonteCarlo":
            self.c = param["c"]
            self.n_simul = param["n_simul"]

    def debut_tour(self, plateau: Plateau, pioche: list, piece_a_jouer: Piece) -> None:
        """
            Utilisé au début du tour pour les IA afin de générer les arbres de jeux, etc...
        """
        if self.type == "MinMax":
            t = time.time()
            score, self.best_move = minimax(plateau, pioche, piece_a_jouer, self.max_depth, evaluate1, float("-inf"), float("inf"), maximise=True)
            print(f"Score du coup trouvé : {score} (coup : {self.best_move}). Temps de calcul : {(time.time() - t):.3f}s")

        if self.type == "MonteCarlo":
            t = time.time()
            score, self.best_move = mcts(RootState(plateau, pioche, piece_a_jouer), self.c, self.n_simul)
            print(f"Score du coup trouvé : {score} (coup : {self.best_move}). Temps de calcul : {(time.time() - t):.3f}s")

    def choisir_piece(self, plateau, pioche: list):
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
        
        elif self.type == "RandomBot":
            i = random.choice(list(pioche.keys()))
            return i
        elif self.type == "MinMax" or self.type == "MonteCarlo":
            return self.best_move[0]

    def choisir_place(self, plateau, pioche, piece_idx):
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
        
        elif self.type == "RandomBot":
            i = random.choice(plateau.recuperer_cases_vides())
            return i
        elif self.type == "MinMax" or self.type == "MonteCarlo":
            return self.best_move[1]