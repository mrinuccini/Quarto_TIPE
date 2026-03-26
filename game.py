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
        print("PIOCHE ⛏️\n"+"-"*60)
        for key in self.pioche.keys():
            print(f"{key} : {self.pioche[key]}")
        print()

    def afficher_plateau(self):
        print("PLATEAU\n"+"-"*60)
        print(self.plateau)
        print()

    def ask(self):
        "Demande au joueur une pièce"
        cont = True
        while cont:
            i = int(input("Veuillez choisir une pièce : "))
            if i in self.pioche: #Si la pièce est disponible dans la pioche
                cont = False
            else:
                print("Pièce indisponible, veuillez réessayer !")
        return i

    def place(self, piece_idx):
        "Placement d'une pièce"
        cont = True
        while cont:
            i = int(input("Veuillez choisir une position où placer la pièce : "))
            row_idx = i % self.x
            column_idx = i // self.x
            if self.plateau.arr[column_idx][row_idx] == None:
                self.plateau.arr[column_idx][row_idx] = self.pioche[piece_idx]
                del self.pioche[piece_idx]
                self.afficher_plateau()
                self.afficher_pioche()
                cont = False        

    def check(self):
        "Vérifie si un joueur a gagné"
        if self.plateau.verifier_alignements():
            self.continuer = False

    def debut_tour(self, piece_idx=None):
        "Affichage des informations avant de jouer"
        print("/"*80+f"\nTour du Joueur {self.joueur+1}\n"+"-"*17)
        if piece_idx!=None:
            print(f"Pièce à jouer : {self.pioche[piece_idx]}")
        self.afficher_plateau()
        self.afficher_pioche()

    def game_launch(self):
        i = 1
        print(f"PARTIE {i}\n" + "-"*9 + "\n")
        while self.parties_restantes > 0:
            self.game_loop()
            self.parties_restantes -= 1

    def game_loop(self):
        "Boucle de jeu"

        self.init_var() #Initialisation des variables de jeu

        self.continuer = 100 #Condition d'arrêt
        self.joueur = 0 #Joueur en train de jouer

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
        
        print(f"Fin de partie, le joueur {self.joueur+1} a gagné !")


game = Game()