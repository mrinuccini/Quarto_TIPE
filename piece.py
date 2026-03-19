class Piece:
    "Instanciation d'une pièce de jeu"
    def __init__(self, couleur, forme, dessus, taille):
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

    """def __eq__(self, p2):
        """Compare""""""

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