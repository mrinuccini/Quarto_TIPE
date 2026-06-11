from load import *

enable_print = False
write_in_game = True #Si on modifie le fichier resultat.csv en cours de jeu

class Game:
    #Instanciation du jeux
    def __init__(self, x=4, y=4):
        """Paramètres:
                n : entier naturel non nul, nombre de parties à jouer
                x : entier naturel non nul, nombre de colonnes du plateau
                y : entier naturel non nul, nombre de lignes du plateau
        """
        #Assertions
        assert(type(x)==type(y)==int and x>0 and y>0)

        self.zb = Zobrist()
        self.x, self.y = x, y #Nombre de colonnes et de lignes du plateau
        self.ask_name()
        self.ask_load()
        self.game_launch() #On lance le jeu
        self.write() #On écrit le fichier des résultats

    def ask_load(self):
        string = input("Charger une partie (Y/n) (defaut:n) : ")
        if string == "":
            string = "n"
        if string == "Y":
            string2 = input("Quel fichier charger (defaut : resultat) : ")
            if string2 == "":
                string2 = "resultats"
            self.load(string2)
        else:
            self.ask_n_parties()
            self.init_player()
            self.init_launch()

    def load(self, name):
        game_data = get_game_data(name)
        self.parties_totales = game_data.get_n_parties()
        self.init_player()

        for i in range(2):
            j : stat = game_data.get_joueur(i+1)
            j_out : Joueur = self.list_joueurs[i]
            j_out.stat.set_reflexion_time(j.get_reflexion_time())
            j_out.stat.set_partie_rt(j.get_partie_reflexion_time())
            j_out.stat.set_total_rt(j.get_total_reflexion_times())
            if j_out.get_type()=="MinMax":
                j_out.stat.set_prof(j.get_prof())
            self.list_joueurs[i] = j_out

        self.max_tour = game_data.get_max_tour()
        self.wins = game_data.get_victoires()
        self.nulles = game_data.get_n_parties_nulles()
        self.parties_restantes = self.parties_totales - self.wins[0] - self.wins[1] - self.nulles

    def ask_n_parties(self):
        "On demande le nombre de parties à jouer"
        string = input("Nombre de parties (défaut : 1) : ")
        if string == "":
            string = "1"
        self.parties_totales = int(string)

    def ask_name(self):
        "On demande dans quel fichier sauvegarder"
        string = input("Quel nom de fichier où sauvegarder (défaut : resultats) : ")
        if string == "":
            string = "resultats"
        self.name = string

    def get_nb_of_columns(self):
        "Renvoie le nombre de colonnes du plateau"
        return self.x

    def get_nb_of_lines(self):
        "Renvoie le nombre de lignes du plateau"
        return self.y
    
    def init_var(self):
        "Initialise les différentes variables / instanciations du jeu"
        self.plateau = Plateau(self.get_nb_of_columns(), self.get_nb_of_lines()) #Plateau
        self.generer_pioche() #Pioche

    def init_player(self):
        "Paramétrages des joueurs"
        self.list_joueurs = []
        for i in range(2):
            param = {"c":1.41421, "n_simul": 1000, "max_depth":4, "nmix":10}

            type = input(f"Joueur {i+1}, quel type de joueur (Humain, RandomBot, MonteCarlo, MinMax, Mix) : ")
            if type == "":
                type = "Humain"

            if type in ("MonteCarlo", "Mix"):
                c = input(f"Quel paramètre d'exploration c ? (défaut : {param['c']}) ")
                if c != "":
                    param["c"] = float(c)
                n_simul = input(f"Combien d'échantillons ? (défaut : {param['n_simul']}) ")
                if n_simul != "":
                    param["n_simul"] = int(n_simul)
            if type in ("MinMax", "Mix"):
                max_depth = input(f"Quelle profondeur maximale ? (défaut : {param['max_depth']}) ")
                if max_depth != "":
                    param["max_depth"] = int(max_depth)
            if type == "Mix":
                nmix = input(f"Combien de résultats avec MC ? (défaut : {param['nmix']}) ")
                if nmix := "":
                    param["nmix"] = int(nmix)
            self.list_joueurs += [Joueur(type, 1, param)]
            print()

    def generer_pioche(self):
        "Génère la pioche du jeu (initialement remplie de toutes les pièces)"
        self.pioche = {}
        for i in range(self.get_nb_of_columns()*self.get_nb_of_lines()):
            self.pioche[i] = Piece((i//8)%2, (i//4)%2,(i//2)%2, i%2)
    
    def afficher_pioche(self):
        "Affichage la pioche"
        if not enable_print: return

        print("PIOCHE ⛏️\n"+"-"*60)
        for key in self.pioche.keys():
            print(f"{key} : {self.pioche[key]}")
        print()

    def afficher_plateau(self):
        "Affichage du plateau"
        if not enable_print: return

        print("PLATEAU\n"+"-"*60)
        print(self.plateau)
        print()

    def ask_pioche(self):
        "Demande au joueur de sélectionner une pièce dans la pioche"
        i = self.list_joueurs[self.joueur_idx].choisir_piece(self.plateau, self.pioche)
        self.zb.choisir_piece(i)
        return i

    def ask_place(self, piece_idx):
        "Choix du placement de la pièce sur le plateau"
        i = self.list_joueurs[self.joueur_idx].choisir_place(self.plateau, self.pioche, piece_idx)
        self.zb.placer_piece(i)
        return i

    def place(self, place_idx, piece):
        """Placement de la pièce piece dans la pioche à la position place_idx"""
        row_idx = place_idx % self.get_nb_of_columns()
        column_idx = place_idx // self.get_nb_of_columns()
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

    def first_tour(self):
        """
        Affichage des informations du premier tour (choix de la pièce uniquement)
        """
        if enable_print: print("/"*80 + f"\nTour du Joueur {self.joueur_idx+1}\n" + "-"*17)
        self.list_joueurs[self.joueur_idx].debut_tour(self.plateau, self.pioche, None, self.zb)
        self.afficher_plateau()
        self.afficher_pioche()

    def debut_tour(self, piece_idx=None):
        """Affichage des informations de début de tour
        Paramètre :
            piece_idx : indice de la pièce à jouer du joueur dans la pioche 
                        (None s'il n'y en a aucune)
        """
        assert((type(piece_idx)==int and piece_idx>=0) or piece_idx==None)

        piece = self.pioche[piece_idx] if piece_idx != None else None
        if piece_idx != None: del self.pioche[piece_idx]

        if enable_print: print("/"*80 + f"\nTour du Joueur {self.joueur_idx+1}\n" + "-"*17)
        self.list_joueurs[self.joueur_idx].debut_tour(self.plateau, self.pioche, piece, self.zb)
        if piece_idx != None and enable_print:
            print(f"Pièce à jouer : {piece}")
        self.afficher_plateau()
        self.afficher_pioche()

    def init_launch(self):
        self.parties_restantes = self.parties_totales
        self.wins = [0,0]
        self.nulles = 0
        self.max_tour = 0

    def game_launch(self):
        """ Lancement du jeu """
        i = self.parties_totales-self.parties_restantes+1
        
        while self.parties_restantes > 0:
            
            print(f"PARTIE {i}/{self.parties_totales}\n" + "-"*9 + ("\n" if enable_print else ""))

            winner, nb_tour = self.game_loop() #On effectue une partie
            self.max_tour = max(self.max_tour, nb_tour)
            if winner != -1:
                self.wins[winner] += 1
            else:
                self.nulles += 1
            
            if write_in_game==True:
                self.write()

            self.parties_restantes -= 1

            print(("\n\n" if enable_print else "")+"♫"*100)
            i += 1
        print("\n\n"+"-"*50+"\nToutes les parties ont été jouées")

    def write(self):
        "Écrit le fichier des résultats de la simulation"
        f = open(self.name+".csv", "w")
        f.write(f"Nombre de parties total, {self.parties_totales}\n")
        f.write(f"Nombre de parties nulles, {self.nulles}\n")
        f.write(f"Nombre de tour max, {self.max_tour}\n")

        for i in range(2):
            joueur:Joueur = self.list_joueurs[i]
            if joueur.get_type() == "MinMax":
                prof = preparer_matrice_pour_sauvegarde(joueur.stat.get_prof())
                f.write(f"J{i+1} : Pronfondeurs atteintes, {prof}\n")
            f.write(f"J{i+1} : Nombre de victoires, {self.wins[i]}\n")
            f.write(f"J{i+1} : Type de joueur, {joueur.get_type()}\n")

            f.write(f"J{i+1} : Temps total de reflexion, {joueur.stat.get_total_reflexion_times()}\n")
            reflexion_par_partie = preparer_liste_pour_sauvegarde(joueur.stat.get_partie_reflexion_time())
            f.write(f"J{i+1} : Temps de reflexion par partie, {reflexion_par_partie}\n")
            reflexion_par_coup = preparer_matrice_pour_sauvegarde(joueur.stat.get_reflexion_time())
            f.write(f"J{i+1} : Temps de reflexion par coup, {reflexion_par_coup}\n")

    def game_loop(self):
        "Boucle de jeu"
        nb_tour = 0
        self.init_var() #Initialisation des variables de jeu
        for i in range(2):
            self.list_joueurs[i].debut_game()
        self.continuer = 100 #Condition d'arrêt
        self.joueur_idx = 0 #Joueur en train de jouer
        self.egalite = False

        #Choix initial de la pièce
        self.first_tour() #Affichage des informations

        #Lancement de la boucle de jeu
        while self.continuer>0:
            nb_tour += 1

            piece_idx = self.ask_pioche() #Choix de la future pièce à jouer
            piece = self.pioche[piece_idx]
            self.joueur_idx = 1 - self.joueur_idx #Changement de joueur

            if enable_print: print("\n")

            self.debut_tour(piece_idx) #Affichage des informations

            place_idx = self.ask_place(piece_idx) #Choix du placement de la pièce
            self.place(place_idx, piece) #On place la pièce
            self.check() #On vérifie s'il y a victoire ou égalité

            self.continuer -= 1

        if self.egalite == True:
            print("Égalité, il ne reste plus aucune pièce à jouer !")
            return -1, (nb_tour)//2
        
        print(f"Fin de partie, le joueur {self.joueur_idx+1} ({self.list_joueurs[self.joueur_idx].type}) a gagné !")
        return self.joueur_idx, nb_tour