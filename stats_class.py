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