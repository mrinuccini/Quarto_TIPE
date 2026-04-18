"Tests du système de plateau de jeu"
from plateau import Plateau
from piece import Piece

if __name__ == "__main__":
    plateau = Plateau(4, 4)

    print(plateau) # Grille 4x4 avec des None

    plateau.placer_piece(1, 0, Piece(1, 0, 0, 0))
    print(plateau) # Grille 4x4 avec des Nones et une pièce noire carrée lisse petite en (1, 0)

    plateau.placer_piece(0, 2, Piece(0, 0, 0, 1))
    print(plateau) # Grille 4x4 avec des Nones et une pièce noire carrée lisse petite en (1, 0) et une pièce blande carrée lisse grande en (0, 2)

    print(plateau.verifier_alignements()) # False

    plateau.placer_piece(0, 2, Piece(1, 0, 0, 0)) # Erreur : pièce déjà présente
    
    plateau.reinitialiser()
    print(plateau)

    print(plateau.verifier_alignements()) # False (toutes les pièces sont à None)

    plateau.placer_piece(0, 0, Piece(1, 0, 0, 0))
    plateau.placer_piece(1, 0, Piece(1, 0, 0, 0))
    plateau.placer_piece(2, 0, Piece(1, 0, 0, 0))
    plateau.placer_piece(3, 0, Piece(1, 0, 0, 0))
    print(plateau.verifier_alignements()) # True car il y a un aligments sur la ligne 1

    plateau.reinitialiser()

    plateau.placer_piece(0, 0, Piece(1, 0, 0, 0))
    plateau.placer_piece(1, 1, Piece(1, 0, 0, 0))
    plateau.placer_piece(2, 2, Piece(1, 0, 0, 0))
    plateau.placer_piece(3, 3, Piece(1, 0, 0, 0))
    print(plateau.verifier_alignements()) # True car il y a un aligments sur une diagonale

    plateau.reinitialiser()

    plateau.placer_piece(0, 0, Piece(1, 0, 0, 0))
    plateau.placer_piece(0, 1, Piece(1, 0, 0, 0))
    plateau.placer_piece(0, 2, Piece(1, 0, 0, 0))
    plateau.placer_piece(0, 3, Piece(1, 0, 0, 0))
    print(plateau.verifier_alignements()) # True car il y a un aligments sur la ligne 2