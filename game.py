from piece import Piece
from plateau import Plateau


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

        self.parties_restantes = n
        self.x, self.y = x, y
        self.game_launch() #On lance le jeu

    def init_var(self):
        "Initialise les différentes variables / instanciations du jeu"
        self.plateau = Plateau(self.x,self.y) #Plateau
        self.generer_pioche() #Pioche

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

    def ask(self):
        "Demande au joueur de sélectionner une pièce dans la pioche"
        cond = True
        while cond: #On ne s'arrête que quand le joueur a sélectionné une pièce valide
            i = int(input("Veuillez choisir une pièce : "))
            if i in self.pioche: #Si la pièce est disponible dans la pioche
                cond = False
            else:
                print("Pièce indisponible, veuillez réessayer !")
        return i

    def place(self, piece_idx):
        "Placement de la pièce d'indice dans la pioche piece_idx sur le plateau"
        assert(type(piece_idx) == int and piece_idx>=0)

        #Sélection de la position
        cond = True
        while cond: #On ne s'arrête que quand le joueur choisi une position valide
            i = int(input("Veuillez choisir une position où placer la pièce : "))
            row_idx = i % self.x
            column_idx = i // self.x
            if self.plateau.arr[column_idx][row_idx] == None:
                cond = False

        #Placement de la pièce
        self.plateau.arr[column_idx][row_idx] = self.pioche[piece_idx]
        del self.pioche[piece_idx]
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
        print("/"*80 + f"\nTour du Joueur {self.joueur+1}\n" + "-"*17)
        if piece_idx != None:
            print(f"Pièce à jouer : {self.pioche[piece_idx]}")
        self.afficher_plateau()
        self.afficher_pioche()

    def game_launch(self):
        """ Lancement du jeu """
        i = 1
        print(f"PARTIE {i}\n" + "-"*9 + "\n")
        while self.parties_restantes > 0:
            self.game_loop()
            self.parties_restantes -= 1
        print("Toutes les parties ont été jouées")

    def game_loop(self):
        "Boucle de jeu"

        self.init_var() #Initialisation des variables de jeu

        self.continuer = 100 #Condition d'arrêt
        self.joueur = 0 #Joueur en train de jouer
        self.egalite = False

        #Choix initial de la pièce
        self.debut_tour() #Affichage des informations

        #Lancement de la boucle de jeu
        while self.continuer>0:
            piece_idx = self.ask()
            self.joueur = 1 - self.joueur #Changement de joueur
            print("\n")
            self.debut_tour(piece_idx) #Affichage des informations
            self.place(piece_idx)
            self.check()

            self.continuer -= 1
        if self.egalite == True:
            print("Égalité, il ne reste plus aucune pice à jouer !")
        else:
            print(f"Fin de partie, le joueur {self.joueur+1} a gagné !")


game = Game()