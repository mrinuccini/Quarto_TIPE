from plateau import Plateau
from piece import Piece

if __name__ == "__main__":
    plateau = Plateau(4, 4)

    print(plateau) # Grille 4x4 avec des None

    plateau.placer_piece(1, 0, Piece(1, 0, 0, 0))
    print(plateau) # Grille 4x4 avec des Nones et une pièce noire carrée lisse petite en (1, 0)

    plateau.placer_piece(1, 0, Piece(1, 0, 0, 0))
    print(plateau) # Grille 4x4 avec des Nones et une pièce noire carrée lisse petite en (1, 0)



