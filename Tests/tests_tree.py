from Tree import *

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

tests()