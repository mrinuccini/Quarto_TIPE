import copy
from math import inf
from plateau import Plateau
from Tree import Node
from piece import Piece, comp
from toolbox import nombre_caracteristiques_communes

def generate_minmax_tree(root: Node, plateau: Plateau, pioche: list, piece_a_placer: Piece, max_depth: int) -> None:
    if max_depth == -1: # On est arrivé à la profondeur souhaitée
        return

    for case in plateau.recuperer_cases_vides():
        # Etape 1 : On génère tous les plateaux possible avec la piece à placer
        clone = plateau.cloner()
        clone.placer_piece_1D(case, piece_a_placer)

        if clone.verifier_alignements(): # Si le placement mène à la victoire, inutile de générer les noeuds avec les différentes pièces à placer
            root.insert(Node((clone, None)))
            continue

        # Pour chacun de ces plateaux, on génère tout les sous plateaux avec les pièces à donner
        for piece_a_donner in pioche:
            child = Node((clone, pioche, piece_a_donner))
            root.insert(child)

            nouvelle_pioche = [p for p in pioche if p != piece_a_donner]
            generate_minmax_tree(child, clone, nouvelle_pioche, piece_a_donner, (max_depth - 1))

# /!\ Pour l'instant, algorithme sans elagage
def minimax(node: Node, maximise: bool, f_eval) -> None:
    successors = node.get_enfants_directs()
    
    if len(successors) == 0: 
        return f_eval(node.val[0], node.val[1], node.val[2])
    else:
        if maximise:
            return max(map(lambda x: minimax(x, false), successors))
        else:
            return min(map(lambda x: minimax(x, false), successors))


def evaluate1(plateau: Plateau, pioche: list, piece_a_donner: Piece):
    # Premièrement, on vérifie si la pièce donnée mène à la victoire
    for case in plateau.recuperer_cases_vides():
        plateau.placer_piece_1D(case, piece_a_donner)

        if plateau.verifier_alignements(): # Si oui, ce coup est catastrophique et on renvoie la plus grande valeur possible
            return -inf

        plateau.placer_piece_1D(case, None)
    
    score = 0

    # Ensuite, on va analyser toutes les lignes et diagonales
    lcds = plateau.recuperer_lignes_diagonales()

    for lcd in lcds:
        pieces_non_vides = [p for p in p if p != None]
        if len(pieces_non_vides) <= 1: # Si la ligne est vide ou n'a qu'une seule pièce, elle ne rapporte rien
            continue

        caracteristiques_communes = nombre_caracteristiques_communes(pieces_non_vides)

        if(caracteristiques_communes == 0): # Cette ligne est morte et ne rapportera rien pour le reste de la partie
            continue

        if(len(pieces_non_vides) == 2):
            score += 10 * caracteristiques_communes # On ajoute 10 points par caractéristiques en commun de la ligne
        elif len(pieces_non_vides) == 3:
            # On compte le nombre de piece dans la pioche qui ont une caractéristiques en commun avec la ligne et on ajoute 100 points pour chacune de ses pièces
            count = 0
            for piece in pioche:
                all_pieces = list(pieces_non_vides)
                all_pieces.append(piece)
                if comp(all_pieces):
                    count += 1

            score += 100 * count
    
    return score


def minmax_place_piece(plateau: Plateau, piece: Piece):
    pass

def minmax_choose_piece(plateau: Plateau, pioche: list) -> int:
    pass


def tests() -> None:
    pass