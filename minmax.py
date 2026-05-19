#Importations
from plateau import *
from Tree import *
from math import inf
from zobrist import Zobrist
from random import randrange, choice
import time

class TimeOutException(Exception):
    """
    Exception levée Quand MinMax a dépassé le temps impparti pour sa recherche
    """
    pass


SCORE_VICTOIRE = 100000
transposition_table = {}

def minmax_premier_coup(plateau: Plateau, pioche: dict, piece_a_placer: Piece) -> tuple:
    """
        Etant donné que le premier coup est souvent le plus long à trouver (presque 200s à la profondeur 5),
        On implémente ici une heuristique basique car il n'est absolument pas nécessaire de passer autant de temps sur ce coup
    """
    # On joue en premier, on renvoie juste une pièce au hasard
    if piece_a_placer is None:
        return Move(None, randrange(0, 15))
    
    # Sinon, on place la pièce donnée à un endroit stratégique (de préférence un coin libre)
    case_choisie = 0
    while plateau.recuperer_piece_1D(case_choisie) is not None:
        case_choisie = choice([0, 15, 12, 3])

    # Pour la pièce à donner, on choisit celle avec le moins de caractéristique en commun par rapport à la pièce à placer (pour éviter de ce mettre dans une situation risquée)
    min_piece_score = 100
    min_piece_id = 0
    for piece_id, piece in list(pioche.items()):
        if nombre_caracteristiques_communes([piece, piece_a_placer]) < min_piece_score:
            min_piece_id = piece_id

    return 0, Move(case_choisie, min_piece_id)


def minimax(plateau: Plateau, pioche: dict, piece_a_placer: Piece, max_depth: int, f_eval, alpha: int, beta: int, zb: Zobrist, t_start: float, t_max: float, maximise: bool=True) -> tuple:
    """
        Applique l'algorithme minmax à l'arbre de racine node

        Présence d'un élagage alpha et beta ainsi que d'une prise en compte des symétries/transpositions
    """

    if time.time() - t_start > t_max:
        raise TimeOutException

    if max_depth == 0 or len(plateau.recuperer_cases_vides()) == 0: 
        return f_eval(plateau, pioche, piece_a_placer) * (-1 if maximise else 1), Move(None, None)
    else:
        meilleur_coup = None
        coup_prioritaire = None

        if zb.get_canonical_hash() in transposition_table:
            data = transposition_table[zb.get_canonical_hash()]
            if data["profondeur"] >= max_depth:
                return data["score"], data["move"]
            
            coup_prioritaire = data["move"] # Move ordering de qualité

        if maximise:
            max_eval = -200000

            if coup_prioritaire is not None and coup_prioritaire.place is not None:
                place_prio = coup_prioritaire.place
                piece_id_prio = coup_prioritaire.piece_idx
                                        
                piece = pioche[piece_id_prio]
                # Si le coup prioritaire est légal
                if plateau.recuperer_piece_1D(place_prio) is None and piece_id_prio in pioche.keys():
                    plateau.placer_piece_1D(place_prio, piece_a_placer)

                    if plateau.verifier_alignements():
                        plateau.placer_piece_1D(place_prio, None)
                        return SCORE_VICTOIRE + max_depth, Move(place_prio, None) # le fait d'ajouter max_depth permet de s'assurer que minmax préferera un coup qui mène rapidement à la victoire plutôt qu'on coup qui mène doucement à la victoire

                    del pioche[piece_id_prio]
                        
                    hash_sauvegarde = list(zb.hash_actuels)
                    piece_en_main_sauvegarde = zb.piece_en_main
                    zb.jouer_coup(place_prio, piece_id_prio)
                    try:
                        f_score, _ = minimax(plateau, pioche, piece, (max_depth - 1), f_eval, max(alpha, max_eval), beta, zb, t_start, t_max, maximise=False)

                        if f_score > max_eval:
                            max_eval = f_score
                            meilleur_coup = Move(place_prio, piece_id_prio) #+
                            #- meilleur_coup = (piece_id, case)

                        if max_eval >= beta:
                            plateau.placer_piece_1D(place_prio, None) # Backtracking on annule le coup qu'on avait joué
                            return max_eval, meilleur_coup

                    finally:
                        plateau.placer_piece_1D(place_prio, None) # Backtracking on annule le coup qu'on avait joué

                        pioche[piece_id_prio] = piece # backtracking, on annule la pièce qu'on avait choisit
                        
                        zb.hash_actuels = hash_sauvegarde
                        zb.piece_en_main = piece_en_main_sauvegarde


            for case in plateau.recuperer_cases_vides():

                plateau.placer_piece_1D(case, piece_a_placer)

                try:
                    if plateau.verifier_alignements():
                        plateau.placer_piece_1D(case, None)
                        return SCORE_VICTOIRE + max_depth, Move(case, None) # le fait d'ajouter max_depth permet de s'assurer que minmax préferera un coup qui mène rapidement à la victoire plutôt qu'on coup qui mène doucement à la victoire
                    
                    for piece_id, piece in list(pioche.items()):
                        if coup_prioritaire is not None and coup_prioritaire.place == case and coup_prioritaire.piece_idx == piece_id:
                            continue

                        del pioche[piece_id]
                        hash_sauvegarde = list(zb.hash_actuels)
                        piece_en_main_sauvegarde = zb.piece_en_main
                        zb.jouer_coup(case, piece_id)

                        try:
                            f_score, _ = minimax(plateau, pioche, piece, (max_depth - 1), f_eval, max(alpha, max_eval), beta, zb, t_start, t_max, maximise=False)

                            if f_score > max_eval:
                                max_eval = f_score
                                meilleur_coup = Move(case, piece_id) #+
                                #- meilleur_coup = (piece_id, case)

                            if max_eval >= beta:
                                plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué
                                return max_eval, meilleur_coup
                        finally:
                            pioche[piece_id] = piece # backtracking, on annule la pièce qu'on avait choisit
                            
                            zb.hash_actuels = hash_sauvegarde
                            zb.piece_en_main = piece_en_main_sauvegarde
                finally:
                    plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué

            transposition_table[zb.get_canonical_hash()] = {"profondeur": max_depth, "score": max_eval, "move": meilleur_coup}
            return max_eval, meilleur_coup
        else:
            min_eval = 200000


            if coup_prioritaire is not None and coup_prioritaire.place is not None:
                place_prio = coup_prioritaire.place
                piece_id_prio = coup_prioritaire.piece_idx                  
                piece = pioche[piece_id_prio]
                
                # Si le coup prioritaire est légal
                if plateau.recuperer_piece_1D(place_prio) is None and piece_id_prio in pioche.keys():
                    plateau.placer_piece_1D(place_prio, piece_a_placer)

                    if plateau.verifier_alignements():
                        plateau.placer_piece_1D(place_prio, None)    
                        return -SCORE_VICTOIRE - max_depth, Move(place_prio, None) # le fait d'ajouter max_depth permet de s'assurer que minmax préferera un coup qui mène rapidement à la victoire plutôt qu'on coup qui mène doucement à la victoire
                    
                    del pioche[piece_id_prio]
                        
                    hash_sauvegarde = list(zb.hash_actuels)
                    piece_en_main_sauvegarde = zb.piece_en_main
                    zb.jouer_coup(place_prio, piece_id_prio)

                    try:
                        f_score, _ = minimax(plateau, pioche, piece, (max_depth - 1), f_eval, max(alpha, min_eval), beta, zb, t_start, t_max, maximise=False)

                        if f_score < min_eval:
                            min_eval = f_score
                            meilleur_coup = Move(place_prio, piece_id_prio) #+
                            #- meilleur_coup = (piece_id, case)

                        if min_eval <= alpha:
                            plateau.placer_piece_1D(place_prio, None) # Backtracking on annule le coup qu'on avait joué
                            return min_eval, meilleur_coup
                        
                    finally:
                        pioche[piece_id_prio] = piece # backtracking, on annule la pièce qu'on avait choisit
                        
                        zb.hash_actuels = hash_sauvegarde
                        zb.piece_en_main = piece_en_main_sauvegarde
                        plateau.placer_piece_1D(place_prio, None) # Backtracking on annule le coup qu'on avait joué

            for case in plateau.recuperer_cases_vides():
                plateau.placer_piece_1D(case, piece_a_placer)

                try:
                    if plateau.verifier_alignements():
                        plateau.placer_piece_1D(case, None)
                        return -SCORE_VICTOIRE - max_depth, Move(case, None) # le fait d'enlever max_depth permet de s'assurer que minmax préferera un coup qui mène rapidement à la victoire plutôt qu'on coup qui mène doucement à la victoire

                    for piece_id, piece in list(pioche.items()):
                        if coup_prioritaire is not None and coup_prioritaire.place == case and coup_prioritaire.piece_idx == piece_id:
                            continue

                        del pioche[piece_id]

                        hash_sauvegarde = list(zb.hash_actuels)
                        piece_en_main_sauvegarde = zb.piece_en_main
                        zb.jouer_coup(case, piece_id)

                        try:
                            f_score, _ = minimax(plateau, pioche, piece, (max_depth - 1), f_eval, alpha, min(beta, min_eval), zb, t_start, t_max, maximise=True)

                            if f_score < min_eval:
                                min_eval = f_score
                                meilleur_coup = Move(case, piece_id) #+
                                #- meilleur_coup = (piece_id, case)

                            if min_eval <= alpha:
                                plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué
                                return min_eval, meilleur_coup
                        finally:
                            pioche[piece_id] = piece # backtracking, on annule la pièce qu'on avait choisit
                            zb.hash_actuels = hash_sauvegarde
                            zb.piece_en_main = piece_en_main_sauvegarde

                finally:
                    plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué

            transposition_table[zb.get_canonical_hash()] = {"profondeur": max_depth, "score": min_eval, "move": meilleur_coup}
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
                return -SCORE_VICTOIRE

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