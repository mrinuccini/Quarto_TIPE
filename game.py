from piece import Piece
from plateau import Plateau


class Game:
    #Instanciation du jeu
    def __init__(self, x=4, y=4):
        self.x = x
        self.y = y
        self.init_var()

    def init_var(self):
        #Plateau
        self.plateau = Plateau(self.x,self.y)
        self.afficher_plateau()

        #Pioche
        self.generer_pioche()
        self.afficher_pioche()

        #On lance la boucle de jeu
        self.game_loop()

    def generer_pioche(self):
        "Génère la pioche du jeu (initialement remplie de toutes les pièces)"
        self.pioche = {}

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    for l in range(2):
                        self.pioche[i*8+j*4+k*2+l] = Piece(i,j,k,l)
    
    def afficher_pioche(self):
        print("PIOCHE ⛏️\n"+"-"*70)
        for key in self.pioche.keys():
            print(f"{key} : {self.pioche[key]}")
        print()

    def afficher_plateau(self):
        print("PLATEAU\n"+"-"*70)
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
        print(f"Tour du Joueur {self.joueur+1}")
        if piece_idx!=None:
            print(f"Pièce à jouer : {self.pioche[piece_idx]}")
        self.afficher_plateau()
        self.afficher_pioche()

    def game_loop(self):
        "Boucle de jeu"
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