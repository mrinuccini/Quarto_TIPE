from Queue import *

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

tests()