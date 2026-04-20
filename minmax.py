import copy
from math import inf
from plateau import Plateau
from Tree import Node
from piece import Piece, comp
from toolbox import nombre_caracteristiques_communes

def minimax(plateau: Plateau, pioche: dict, piece_a_placer: Piece, max_depth: int, f_eval, alpha, beta, maximise: bool=True) -> tuple:
    """
        Applique l'algorithme minmax à l'arbre de racine node

        Pour l'instant, algorithme uniquement avec un elagage alpha-beta classique (pas de prise en compte des symétries)
    """

    if max_depth == 0 or len(plateau.recuperer_cases_vides()) == 0: 
        return f_eval(plateau, pioche, piece_a_placer) * (-1 if maximise else 1), (None, None)
    else:
        meilleur_coup = None

        if maximise:
            max_eval = float("-inf")

            for case in plateau.recuperer_cases_vides():
                plateau.placer_piece_1D(case, piece_a_placer)

                if plateau.verifier_alignements():
                    plateau.placer_piece_1D(case, None)
                    return f_eval(plateau, pioche, piece_a_placer) * (-1 if maximise else 1), (None, case)
                
                for piece_id, piece in list(pioche.items()):
                    del pioche[piece_id]
                    
                    f_score, _ = minimax(plateau, pioche, piece, (max_depth - 1), f_eval, max(alpha, max_eval), beta, maximise=False)
                    pioche[piece_id] = piece # backtracking, on annule la pièce qu'on avait choisit
                    
                    if f_score > max_eval:
                        max_eval = f_score
                        meilleur_coup = (piece_id, case)

                    if max_eval >= beta:
                        plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué
                        return max_eval, meilleur_coup

                plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué

            return max_eval, meilleur_coup
        else:
            min_eval = float("inf")

            for case in plateau.recuperer_cases_vides():
                plateau.placer_piece_1D(case, piece_a_placer)

                if plateau.verifier_alignements():
                    plateau.placer_piece_1D(case, None)
                    return f_eval(plateau, pioche, piece_a_placer) * (-1 if maximise else 1), (None, case)
                
                for piece_id, piece in list(pioche.items()):
                    del pioche[piece_id]

                    f_score, _ = minimax(plateau, pioche, piece, (max_depth - 1), f_eval, alpha, min(beta, min_eval), maximise=True)
                    
                    pioche[piece_id] = piece # backtracking, on annule la pièce qu'on avait choisit

                    if f_score < min_eval:
                        min_eval = f_score
                        meilleur_coup = (piece_id, case)

                    if min_eval <= alpha:
                        plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué
                        return min_eval, meilleur_coup

                plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué

            return min_eval, meilleur_coup

def evaluate1(plateau: Plateau, pioche: list, piece_a_donner: Piece):
    """
        Fonction d'évalution n°1 pour l'algorithme minmax

        Principe : 
        si la piece à donner mêne à la victoire on renvoie une valeur gigantesque
        Sinon, plus il y a de ligne avec de caractéristique en commun, plus le score sera élevé
        De plus, si une ligne possède 3 pièce avec des caractéristiques en commun, plus il y a de pièce dans la pioche qui permettraient de compléter la ligne, plus le score sera élevé
    """
    score = 0

    # Ensuite, on va analyser toutes les lignes et diagonales
    lcds = plateau.recuperer_lignes_diagonales()

    for lcd in lcds:
        pieces_non_vides = [p for p in lcd if p != None]
        if len(pieces_non_vides) <= 1: # Si la ligne est vide ou n'a qu'une seule pièce, elle ne rapporte rien
            continue

        # On vérifie si la pièce donnée par l'adversaire mène directement à un échec
        if len(pieces_non_vides) == 3:
            if comp(pieces_non_vides + [piece_a_donner]):
                return float("inf")

        caracteristiques_communes = nombre_caracteristiques_communes(pieces_non_vides)

        if(caracteristiques_communes == 0): # Cette ligne est morte et ne rapportera rien pour le reste de la partie
            continue

        if(len(pieces_non_vides) == 2):
            score += 10 * caracteristiques_communes # On ajoute 10 points par caractéristiques en commun de la ligne
        elif len(pieces_non_vides) == 3:
            # On compte le nombre de piece dans la pioche qui ont une caractéristiques en commun avec la ligne et on ajoute 100 points pour chacune de ses pièces
            count = 0
            for piece_pioche in pioche.values(): 
                if comp(pieces_non_vides + [piece_pioche]):
                    count += 1

            score += 100 * count
    
    return score