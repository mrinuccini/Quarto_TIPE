class stat:
    "Instanciation des stats (associées à un joueur)"
    def __init__(self):
        self.total_reflexion_time = 0 #temps de réflexion total
        self.partie_rt = [] #temps de réflexion total par partie
        self.rt = [] #temps de réflexion par coup et par partie
        self.n = -1 #numéro de partie actuelle

    def deb_partie(self):
        self.partie_rt += [0]
        self.rt += [[]]
        self.n += 1

    def act(self, duree:float):
        "Rajoute un coup de duree secondes pour la partie actuelle"
        self.total_reflexion_time += duree
        self.partie_rt[self.n] += duree
        self.rt[self.n] += [duree]

    def get_total_reflexion_times(self):
        "Renvoie le temps de réflexion total"
        return self.total_reflexion_time
    
    def get_partie_reflexion_time(self):
        "Renvoie le temps de réflexion par partie"
        return self.partie_rt
    
    def get_reflexion_time(self):
        "Renvoie le temps de réflexion par partie et par coup"
        return self.rt
    
    def set_reflexion_time(self, rt):
        "Modifie le temps de réflexion par partie et par coup"
        self.rt = rt

    def set_partie_rt(self, partie_rt):
        "Modifie le temps de réflexion par partie"
        self.partie_rt = partie_rt

    def set_total_rt(self, total_rt):
        "Modifie le temps de réflexion total"


class Game_data:
    def __init__(self):
        self.n = 0 #Nombre de parties totales
        self.n_nulles = 0 #Nombre de parties nulles
        self.victoires = [] #Nombre de victoires par joueur
        self.joueurs = []
        self.max_tour = 0

    def set_nb_parties(self, n):
        "Modifie le nombre de parties totales"
        self.n = n

    def set_n_nulles(self, n_nulles):
        "Modifie le nombre de parties nulles"
        self.n_nulles = n_nulles

    def set_max_tour(self, max_tour):
        "Modifie le nombre de tour max"
        self.max_tour = max_tour

    def push_victoires(self,  n_vic):
        "Rajoute un nombre de victoires"
        self.victoires += [n_vic]

    def push_joueur(self, joueur_data):
        "Rajoute les datas d'un joueur"
        self.joueurs += [joueur_data]

    def get_n_parties(self):
        "Renvoie le nombre de parties totales"
        return self.n
    
    def get_n_parties_nulles(self):
        "Renvoie le nombre de parties nulles"
        return self.n_nulles
    
    def get_joueur(self, i):
        "Renvoie le joueur i"
        return self.joueurs[i-1]
    
    def get_victoires(self):
        "Renvoie le nombre de victoire par joueur"
        return self.victoires
    
    def get_max_tour(self):
        "Renvoie le nombre de tour max"
        return self.max_tour