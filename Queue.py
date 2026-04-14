"Instanciation d'une file"
class Cellule:
    "Instanciation d'une cellule"
    def __init__(self, val, suivant=None):
        assert(suivant == None or type(suivant) == Cellule)
        self.val = val
        self.suivant = suivant

    def __repr__(self):
        return f"{self.val}"
    

class Queue:
    "instanciation d'une file"
    def __init__(self):
        self.first = None
        self.last = None

    def est_vide(self):
        "Renvoie si la file est vide"
        return self.first == None

    def enqueue(self, val):
        "Enfilement"
        cell = Cellule(val)
        if self.last == None:
            self.first = cell
        else:
            self.last.suivant = cell
        self.last = cell

    def dequeue(self):
        "Défilement"
        assert(not(self.est_vide()))
        cell = self.first
        self.first = self.first.suivant
        if self.first == None:
            self.last = None
        return cell.val
    
    def __repr__(self):
        "Affichage de la file"
        str = ""
        cell = self.first
        while cell != None:
            str += f"{cell.val} →"
            cell = cell.suivant
        return str
    

##Tests
def tests():
    "Test de la pile"
    p = Queue()
    print(p.est_vide())
    p.enqueue(5)
    print(p)
    print()
    p.enqueue(8)
    print(p)
    print()
    p.enqueue(12)
    print(p)
    print()
    p.dequeue()
    print(p)
    print()
    p.enqueue(13)
    print(p)
    print()
    for i in range(3):
        p.dequeue()
        print(p)
        print()
    print(p.est_vide())