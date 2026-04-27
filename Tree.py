"Instanciaiton d'arbres"
from Queue import *
from math import log

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
        #assert(type(enfants)==list and all(type(e)==Node for e in enfants))
        # assert(type(val)==float)

        self.val = val
        self.enfants = enfants

    def insert(self, node):
        """Insère le nœud node à la racine
            Paramètres :
                - node : Node
        """
        #assert(type(node)==Node)
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
    

class Node_MCTS(Node):
    "Instanciation d'un nœud pour MCTS"
    def __init__(self, val, move=None, enfants=None, parent=None):
        """ Paramètres :
                - val : float
                        valeur du nœud
                - enfants : liste des enfants
                - parent : parent du noued
        """
        super().__init__(val, enfants) #Initialisation classique d'un arbre

        self.parent = parent
        self.win = 0 #Nombre de victoires associé au noeud
        self.visited = 0 #Nombre de visites du noeud
        self.move = move #mouvement associé au noeud
        
    def insert(self, node):
        super().insert(node)
        node.parent = self
    
    def init_tree_for_mcts(self):
        """ Prépare l'arbre pour le MCTS """
        self.win = 0
        self.visited = 0
        for e in self.enfants:
            e.init_tree_for_mcts()
                
    def get_ucb(self, c):
        """ Renvoie le UCT associé au noeud, au paramètre d'exploration c """
        if self.visited == 0:
            return float('inf')
        return self.win / self.visited + c * log(self.parent.visited) / self.visited

    def get_parent(self):
        "Renvoie le parent du noeud"
        return self.parent