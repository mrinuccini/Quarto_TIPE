class Piece:
    "Instanciation d'une pièce de jeu"
    def __init__(self, couleur, forme, dessus, taille):
        """Paramètres :
                couleur : 0 ou 1, couleur de la pièce (0=blanc, 1=noir)
        """
        self.couleur = couleur