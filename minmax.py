import copy
from math import inf
from plateau import Plateau
from Tree import Node
from piece import Piece, comp
from toolbox import nombre_caracteristiques_communes

def generate_minmax_tree(root: Node, plateau: Plateau, pioche: dict, piece_a_placer: Piece, max_depth: int) -> None:
    if max_depth == -1: # On est arrivé à la profondeur souhaitée
        return

    for case in plateau.recuperer_cases_vides():
        # Etape 1 : On génère tous les plateaux possible avec la piece à placer
        plateau.placer_piece_1D(case, piece_a_placer)
        
        if plateau.verifier_alignements(): # Si le placement mène à la victoire, inutile de générer les noeuds avec les différentes pièces à placer
            root.insert(Node((None, None, plateau.cloner(), None)))
            plateau.placer_piece_1D(case, None)
            continue

        # Pour chacun de ces plateaux, on génère tout les sous plateaux avec les pièces à donner
        for piece_id, piece in list(pioche.items()):
            child = None

            if max_depth > 0: child = Node((piece_id, case))
            else: child = Node((piece_id, case, plateau.cloner(), pioche))

            root.insert(child)

            del pioche[piece_id]

            generate_minmax_tree(child, plateau, pioche, piece, (max_depth - 1))

            pioche[piece_id] = piece

        plateau.placer_piece_1D(case, None)

def minimax(node: Node, f_eval, alpha, beta, maximise: bool=True) -> tuple:
    """
        Applique l'algorithme minmax à l'arbre de racine node

        Pour l'instant, algorithme uniquement avec un elagage alpha-beta classique (pas de prise en compte des symétries)
    """
    successors = node.get_enfants_directs()
    
    if len(successors) == 0: 
        return f_eval(node.val[2], node.val[3], node.val[3][node.val[0]]) * (1 if maximise else -1), None
    else:
        meilleur_noeud = None

        if maximise:
            max_eval = float("-inf")

            for succ in successors:
                f_score, _ = minimax(succ, f_eval, max_eval, beta, maximise=False)
                if f_score > max_eval:
                    meilleur_noeud = succ
                    max_eval = f_score

                if max_eval >= beta:
                    break

            return max_eval, meilleur_noeud
        else:
            min_eval = float("inf")

            for succ in successors:
                f_score, _ = minimax(succ, f_eval, alpha, min_eval, maximise=True)
                if f_score < min_eval:
                    meilleur_noeud = succ
                    min_eval = f_score

                if min_eval <= alpha:
                    break

            return min_eval, meilleur_noeud


def evaluate1(plateau: Plateau, pioche: list, piece_a_donner: Piece):
    """
        Fonction d'évalution n°1 pour l'algorithme minmax

        Principe : 
        si la piece à donner mêne à la victoire on renvoie une valeur gigantesque
        Sinon, plus il y a de ligne avec de caractéristique en commun, plus le score sera élevé
        De plus, si une ligne possède 3 pièce avec des caractéristiques en commun, plus il y a de pièce dans la pioche qui permettraient de compléter la ligne, plus le score sera élevé
    """
    # Premièrement, on vérifie si la pièce donnée mène à la victoire
    for case in plateau.recuperer_cases_vides():
        plateau.placer_piece_1D(case, piece_a_donner)

        if plateau.verifier_alignements(): # Si oui, ce coup est catastrophique et on renvoie la plus grande valeur possible
            return float("inf")

        plateau.placer_piece_1D(case, None)
    
    score = 0

    # Ensuite, on va analyser toutes les lignes et diagonales
    lcds = plateau.recuperer_lignes_diagonales()

    for lcd in lcds:
        pieces_non_vides = [p for p in lcd if p != None]
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
                all_pieces.append(pioche[piece])
                if comp(all_pieces):
                    count += 1

            score += 100 * count
    
    return score