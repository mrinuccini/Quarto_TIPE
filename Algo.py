from plateau import Plateau
from piece import Piece

class Algorithm:
    """
        Classe de base pour tous les joueurs/algorithmes du jeu
    """
    def choisir_piece(self, plateau: Plateau, pioche: list) -> int:
        """
            Choisit une pièce parmis la liste des pièces disponibles dans la pioche 
            Renvoie l'indice de la pièce choisit dans la pioche
        """
        return 0

    def choisir_place(self, plateau: Plateau, pioche: list, piece: Piece) -> int:
        """
            Choisit un endroit ou placer une pièce sur le plateau.
            Renvoit l'indice de la case sur le plateau
        """
        return 0