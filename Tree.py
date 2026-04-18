"Instanciaiton d'arbres"
from Queue import Queue

class Node:
    "Instanciation d'un nœud"
    def __init__(self, val, enfants=None):
        """ Paramètres :
                - val : float
                        valeur du nœud
                - enfants : liste des enfants
        """
        #Assertions
        if enfants == None:
            enfants = []
        assert(type(enfants)==list and all(type(e)==Node for e in enfants))
        # assert(type(val)==float)

        self.val = val
        self.enfants = enfants

    def insert(self, node):
        """Insère le nœud node à la racine
            Paramètres :
                - node : Node
        """
        assert(type(node)==Node)
        self.enfants += [node]

    def get_enfants(self):
        "Renvoie tous les enfants du nœud (même les petits enfants)"
        L = []
        for enfant in self.enfants:
            L += [enfant]
            L += enfant.get_enfants()
        return L
    
    def get_enfants_directs(self):
        "Renvoie les enfants directs du nœud"
        return self.enfants
    
    def parcours_prefixe(self):
        "Parcours préfixe de l'arbre"
        L = [self.val]
        for e in self.enfants:
            L += e.parcours_prefixe()
        return L

    def parcours_postfixe(self):
        "Parcours postfixe de l'arbre"
        L = []
        for e in self.enfants:
            L += e.parcours_postfixe()
        L += [self.val]
        return L
    
    def parcours_largeur(self):
        "Parcoues par largeur de l'arbre"
        p = Queue()
        p.enqueue(self)
        L = []
        while not(p.est_vide()):
            tete = p.dequeue()
            L += [tete.val]
            for e in tete.enfants:
                p.enqueue(e)
        return L

    def __repr__(self):
        "Représentation"
        return f"{self.val}, {self.enfants}"