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
        assert(type(val)==float)

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
    

def tests():
    t = Node(1.0)
    t.insert(Node(2.0))
    t.insert(Node(3.0))
    t.get_enfants_directs()[0].insert(Node(5.2))
    t.get_enfants_directs()[0].get_enfants_directs()[0].insert(Node(8.23))
    t.get_enfants_directs()[1].insert(Node(13.1))

    print("Parcours largeur")
    print(t.parcours_largeur())
    print("Parcours suffixe")
    print(t.parcours_postfixe())
    print("Parcours préfixe")
    print(t.parcours_prefixe())