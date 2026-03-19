class Piece:
    "Instanciation d'une pièce de jeu"
    def __init__(self, couleur: int, forme: int, dessus: int, taille:int) -> None:
        """Paramètres :
                couleur : 0 ou 1, couleur de la pièce (0=blanc, 1=noir)
                forme : 0 ou 1, forme de la pièce (0=carré, 1=rond)
                dessus : 0 ou 1, dessus de la pièce (0=lisse, 1=creusé)
                taille : 0 ou 1, taille de la pièce (0=petite, 1=grande)
        """
        assert(couleur in (0,1))
        assert(forme in (0,1))
        assert(dessus in (0,1))
        assert(taille in (0,1))
        self.couleur = couleur
        self.forme = forme
        self.dessus = dessus
        self.taille = taille

    def __repr__(self):
        "Affichage de la pièce"
        str = "pièce"
        if self.couleur == 0:
            str += " blanche"
        else:
            str += " noire"

        if self.forme == 0:
            str += " carrée"
        else:
            str += " ronde"

        if self.dessus == 0:
            str += " lisse"
        else:
            str += " creusée"

        if self.taille == 0:
            str += " petite"
        else:
            str += " grande"
        
        return str


def comp(L):
    """Compare une liste de pièces"""
    assert(L!=[])
    assert(type(L)==list)

    if None in L:
         return False
    
    if all(p.couleur == L[0].couleur for p in L[1:]):
            return True
    if all(p.forme == L[0].forme for p in L[1:]):
            return True
    if all(p.dessus == L[0].dessus for p in L[1:]):
            return True
    if all(p.taille == L[0].taille for p in L[1:]):
            return True
    
    return False


def test():
     p1 = Piece(1,1,1,1)
     p2 = Piece(1,0,1,0)
     p3 = Piece(1,0,0,0)
     p4 = Piece(1,1,0,1)
     p5 = Piece(0,0,0,0)
     assert(comp([p1,p2,p3,p4])==True)
     assert(comp([p1,p5,p3,p4])==False)
     assert(comp([p5,p3,p4])==True)


test()