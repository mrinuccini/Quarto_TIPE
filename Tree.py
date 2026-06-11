"Instanciaiton d'arbres"
from Queue import *
from math import log, sqrt
from move import *

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
    def __init__(self, move=None, parent=None):
        """ Paramètres :
                - val : float
                        valeur du nœud
                - move : instanciation de la classe Move, mouvement associé au noeud (un mouvement = une case où placer
                                                          et une pièce à donner)
                - parent : Nod_MCTS, parent du noued
        """
        self.parent = parent #Noeud parent, permet de remonter dans l'arbre
        self.enfants = [] #Noeud enfant
        self.win = 0 #Nombre de victoires associé au noeud
        self.visited = 0 #Nombre de visites du noeud
        self.move = move #mouvement associé au noeud
        self.untried_moves = None #Mouvement non essayés
        
    def get_win_number(self):
        "Renvoie le nombre de victoires associé au noeud"
        return self.win
        
    def increase_win_number(self, val):
        "Augmente le nombre de victoires associé au noeud"
        self.win += val

    def get_visit_number(self):
        "Renvoie le nombre de visites associé au noeud"
        return self.visited
    
    def increase_visit_number(self):
        "Augmente le nombre de visite du noeud"
        self.visited += 1
        
    def get_parent(self):
        "Renvoie le parent du noeud"
        return self.parent
        
    def get_move(self):
        "Renvoie le mouvement associé au noeud"
        return self.move
    
    def gen_untried_moves(self, cases, pieces):
        "Génère les mouvements non essayés selon la liste de cases cases et celle de pieces pieces"
        self.untried_moves = [Move(c, p) for c in cases for p in pieces]


    def get_untried_moves(self):
        "Renvoie les mouvements non essayés"
        return self.untried_moves


    def insert(self, node):
        "Insère node"
        super().insert(node)
        node.parent = self
    
    def init_tree_for_mcts(self):
        """ Prépare l'arbre pour le MCTS """
        self.win = 0
        self.visited = 0
        for e in self.enfants:
            e.init_tree_for_mcts()
                
    def get_ucb(self, c):
        """ Renvoie le UCT associé au noeud, au paramètre d'exploration c :
        c = 1 : autant d'exploration que d'exploitation
        c > 1 : plus d'exploration
        c < 1 : plus d'exploitation
        """
        if self.visited == 0:
            return float('inf')
        if self.parent is None or self.parent.visited == 0:
            return self.win / self.visited
        return self.win / self.visited + c*sqrt(log(self.parent.visited) / self.visited)

    def get_parent(self):
        "Renvoie le parent du noeud"
        return self.parent