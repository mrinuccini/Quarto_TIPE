from player import *
from time import sleep

class Game:
    #Instanciation du jeux
    def __init__(self, n=1, x=4, y=4):
        """Paramètres:
                n : entier naturel non nul, nombre de parties à jouer
                x : entier naturel non nul, nombre de colonnes du plateau
                y : entier naturel non nul, nombre de lignes du plateau
        """
        #Assertions
        assert(type(n)==int and n>0)
        assert(type(x)==type(y)==int and x>0 and y>0)

        self.parties_totales = n
        self.x, self.y = x, y
        self.game_launch() #On lance le jeu
        self.write() #On écrit le fichier des résultats

    def init_var(self):
        "Initialise les différentes variables / instanciations du jeu"
        self.plateau = Plateau(self.x,self.y) #Plateau
        self.generer_pioche() #Pioche

        self.init_player()

    def init_player(self):
        "Paramétrages des joueurs"
        j1_param = {"c":1.4, "n_simul": 1000, "max_depth":4}
        j1_type = input("Joueur 1, quel type de joueur (Humain, RandomBot, MonteCarlo, MinMax) : ")

        if j1_type == "MonteCarlo":
            c = input("Quel paramètre d'exploration c ? (défaut : 1.4) ")
            if c != "":
                j1_param["c"] = int(c)
            n_simul = input("Combien d'échantillons ? (défaut : 1000) ")
            if n_simul != "":
                j1_param["n_simul"] = int(n_simul)
        elif j1_type == "MinMax":
            max_depth = input("Quelle profondeur maximale ? (défaut : 4) ")
            if max_depth != "":
                j1_param["max_depth"] = int(max_depth)

        j2_param = {"c":1.4, "n_simul":1000, "max_depth":4}
        j2_type = input("Joueur 2, quel type de joueur (Humain, RandomBot, MonteCarlo, MinMax) : ")

        if j2_type == "MonteCarlo":
            c = input("Quel paramètre d'exploration c ? (défaut : 1.4) ")
            if c != "":
                j2_param["c"] = int(c)
            n_simul = input("Combien d'échantillons ? (défaut : 1000) ")
            if n_simul != "":
                j2_param["n_simul"] = int(n_simul)
        elif j2_type == "MinMax":
            max_depth = input("Quelle profondeur maximale ? (défaut : 4) ")
            if max_depth != "":
                j2_param["max_depth"] = int(max_depth)

        self.list_joueurs = [Joueur(j1_type, param=j1_param), Joueur(j2_type, param=j2_param)]

    def generer_pioche(self):
        "Génère la pioche du jeu (initialement remplie de toutes les pièces)"
        self.pioche = {}
        for i in range(16):
            self.pioche[i] = Piece((i//8)%2, (i//4)%2,(i//2)%2, i%2)
    
    def afficher_pioche(self):
        "Affichage la pioche"
        print("PIOCHE ⛏️\n"+"-"*60)
        for key in self.pioche.keys():
            print(f"{key} : {self.pioche[key]}")
        print()

    def afficher_plateau(self):
        "Affichage du plateau"
        print("PLATEAU\n"+"-"*60)
        print(self.plateau)
        print()

    def ask_pioche(self):
        "Demande au joueur de sélectionner une pièce dans la pioche"
        i = self.list_joueurs[self.joueur_idx].choisir_piece(self.plateau, self.pioche)
        return i

    def ask_place(self, piece_idx):
        "Choix du placement de la pièce sur le plateau"
        i = self.list_joueurs[self.joueur_idx].choisir_place(self.plateau, self.pioche, piece_idx)
        return i;

    def place(self, place_idx, piece):
        """Placement de la pièce d'indice piece_idx dans la pioche à la position place_idx"""
        row_idx = place_idx % self.x
        column_idx = place_idx // self.x
        #Placement de la pièce

        self.plateau.placer_piece(row_idx, column_idx, piece)

        self.afficher_plateau()
        self.afficher_pioche()

    def check(self):
        "Vérifie si un joueur a gagné"
        if self.plateau.verifier_alignements():
            self.continuer = False
        elif len(self.pioche) == 0: #S'il n'y a plus de pièce à jouer et aucun alignement, égalité
            self.continuer = False
            self.egalite = True

    def debut_tour(self, piece_idx=None):
        """Affichage des informations de début de tour
        Paramètre :
            piece_idx : indice de la pièce à jouer du joueur dans la pioche 
                        (None s'il n'y en a aucune)
        """
        assert((type(piece_idx)==int and piece_idx>=0) or piece_idx==None)

        piece = self.pioche[piece_idx] if piece_idx != None else None
        if piece_idx != None: del self.pioche[piece_idx]

        self.list_joueurs[self.joueur_idx].debut_tour(self.plateau, self.pioche, piece)

        print("/"*80 + f"\nTour du Joueur {self.joueur_idx+1}\n" + "-"*17)
        if piece_idx != None:
            print(f"Pièce à jouer : {piece}")
        self.afficher_plateau()
        self.afficher_pioche()

    def game_launch(self):
        """ Lancement du jeu """
        i = 1
        self.parties_restantes = self.parties_totales
        self.wins = [0,0]

        print(f"PARTIE {i}\n" + "-"*9 + "\n")

        while self.parties_restantes > 0:
            winner = self.game_loop() #On effectue une partie
            self.wins[winner] += 1
            self.parties_restantes -= 1
        print("Toutes les parties ont été jouées")

    def write(self):
        f = open("resultats.csv", "w")
        f.write(f"Nombre de parties total, {self.parties_totales}\n")
        f.write(f"Nombre de parties nulles, {self.parties_restantes - self.wins[0] - self.wins[1]}\n")
        f.write(f"J1 : Nombre de victoires, {self.wins[0]}\n")
        f.write(f"J1 : Temps total de réflexion, {self.list_joueurs[0].reflexion_time}\n")
        f.write(f"J2 : Nombre de victoires, {self.wins[1]}\n")
        f.write(f"J2 : Temps total de réflexion, {self.list_joueurs[1].reflexion_time}\n")

    def game_loop(self):
        "Boucle de jeu"

        self.init_var() #Initialisation des variables de jeu

        self.continuer = 100 #Condition d'arrêt
        self.joueur_idx = 0 #Joueur en train de jouer
        self.egalite = False

        #Choix initial de la pièce
        self.debut_tour() #Affichage des informations

        #Lancement de la boucle de jeu
        while self.continuer>0:
            piece_idx = self.ask_pioche() #Choix de la future pièce à jouer
            piece = self.pioche[piece_idx]
            self.joueur_idx = 1 - self.joueur_idx #Changement de joueur

            print("\n")

            self.debut_tour(piece_idx) #Affichage des informations

            place_idx = self.ask_place(piece_idx) #Choix du placement de la pièce
            self.place(place_idx, piece) #On place la pièce
            self.check() #On vérifie s'il y a victoire ou égalité

            self.continuer -= 1
        if self.egalite == True:
            print("Égalité, il ne reste plus aucune pièce à jouer !")
            return -1
        print(f"Fin de partie, le joueur {self.joueur_idx+1} a gagné !")
        return self.joueur_idx