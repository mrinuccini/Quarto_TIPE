"Instanciation des joueurs"

#Importations
from minmax import *
from montecarlo import *
from xterminator import *
import random
import time
import pickle
import os

TYPES = ["Humain", "MonteCarlo", "MinMax", "RandomBot", "Mix"]

class Joueur:
    def __init__(self, typ="Humain", niveau=1, param={}):
        global transposition_table
        """ Paramètre :
                type : chaîne de caractères, élément de TYPES
                       type de joueur
                niveau : entier naturel
                         niveau de l'IA (si non humain)
        """
        #assert(typ in TYPES)
        self.type = typ
        self.niveau = niveau

        self.reflexion_time = 0 #Temps de réflexion total sur la partie

        self.best_move :Move= None #Meilleur mouvement

        if self.type == "MinMax" or self.type == "Mix":
            self.max_depth = param["max_depth"]
            if os.path.isfile("transpositions.tbl"):
                with open("transpositions.tbl", 'rb') as tbl:
                    transposition_table = pickle.load(tbl)
                    print(f"loaded transposition table of size : {len(transposition_table)}")
        if self.type == "MonteCarlo" or self.type=="Mix":
            self.c = param["c"]
            self.n_simul = param["n_simul"]
        if self.type == "Mix":
            self.nmix = param['nmix']

    def debut_tour(self, plateau: Plateau, pioche: list, piece_a_jouer: Piece, zb: Zobrist) -> None:
        """
            Utilisé au début du tour pour les IA afin de générer les arbres de jeux, etc...
        """
        if self.type in ("MinMax", "MonteCarlo", "Mix"):
            t1 = time.time()

            match self.type:
                case "MinMax":
                    if len(pioche) > 13:
                        score, self.best_move = minmax_premier_coup(plateau, pioche, piece_a_jouer)
                    else:
                        score = 0
                        meilleur_coup_global = None

                        try:
                            for profondeur in range(1, 16):
                                score, meilleur_coup_profondeur = minimax(plateau, pioche, piece_a_jouer, profondeur, evaluate1, float("-inf"), float("inf"), zb, t1, 45, maximise=True)
                                
                                if meilleur_coup_profondeur is not None:
                                    meilleur_coup_global = meilleur_coup_profondeur
                                    self.best_move = meilleur_coup_global
                                    
                                print(f"Profondeur {profondeur} atteinte.")
                        except TimeOutException:
                            print("Temps écoulé !")
                case "MonteCarlo":
                    scores, self.best_moves = mcts(RootState(plateau, pioche, piece_a_jouer), self.c, self.n_simul)
                    self.best_move = self.best_moves[0]
                    score = scores[0]
                case "Mix":
                    score, self.best_move = xterminator(RootState(plateau, pioche, piece_a_jouer), self.c, self.n_simul, self.nmix, self.max_depth)
            
            t2 = time.time()
            delta_t = t2 - t1
            self.reflexion_time += delta_t

            print(f"Score du coup trouvé : {score} (coup : {self.best_move}). Temps de calcul : {(delta_t):.3f}s")

    def choisir_piece(self, plateau, pioche: list):
        """ Choix d'une pièce que devra placer le joueur suivant, selon le type du joueur """
        #Joueur humain
        if self.type == "Humain":
            t1 = time.time()
            cond = True
            while cond: #On ne s'arrête que quand le joueur a sélectionné une pièce valide
                i = int(input("Veuillez choisir une pièce : "))
                if i in pioche: #Si la pièce est disponible dans la pioche
                    cond = False
                else:
                    print("Pièce indisponible, veuillez réessayer !")
            t2 = time.time()
            delta_t = t2 - t1
            self.reflexion_time += delta_t
            return i
        
        elif self.type == "RandomBot":
            i = random.choice(list(pioche.keys()))
            return i
        
        elif self.type in ("MinMax", "MonteCarlo", "Mix"):
            if self.best_move == None or self.best_move.get_piece_idx() == None:
                return random.choice(list(pioche.keys()))
            else:
                return self.best_move.get_piece_idx()

    def choisir_place(self, plateau, pioche, piece_idx):
        """ Choix du placement de la pièce selon le type du joueur """
        #Joueur humain
        if self.type == "Humain":
            t1 = time.time()
            #Sélection de la position
            cond = True
            while cond: #On ne s'arrête que quand le joueur choisi une position valide
                i = int(input("Veuillez choisir une position où placer la pièce : "))
                row_idx = i % plateau.x
                column_idx = i // plateau.x
                if plateau.arr[column_idx][row_idx] == None:
                    cond = False
            t2 = time.time()
            delta_t = t2 - t1
            self.reflexion_time += delta_t
            return i
        
        elif self.type == "RandomBot":
            i = random.choice(plateau.recuperer_cases_vides())
            return i
        
        elif self.type in ("MinMax", "MonteCarlo", "Mix"):
            if self.best_move == None or self.best_move.get_place() == None:
                return random.choice(plateau.recuperer_cases_vides())
            else:
                return self.best_move.get_place()