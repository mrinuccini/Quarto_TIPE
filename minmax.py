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

MAX_HISTORY = 16384
history = [0] * 256

def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n

def update_history(case_id: int, piece_a_donner_id: int, bonus):
    """
        cf. https://webdocs.cs.ualberta.ca/~jonathan/publications/ai_publications/pami.pdf
        cf. https://www.chessprogramming.org/History_Heuristic pour le history gravity formula
    """
    id_coup = (case_id * 16) + piece_a_donner_id

    clamped_bonus = clamp(bonus, -MAX_HISTORY, MAX_HISTORY)
    history[id_coup] += clamped_bonus - history[id_coup] * abs(clamped_bonus) // MAX_HISTORY # History gravity formula



def minmax_premier_coup(plateau: Plateau, pioche: dict, piece_a_placer: Piece) -> tuple:
    """
        Etant donné que le premier coup est souvent le plus long à trouver (presque 200s à la profondeur 5),
        On implémente ici une heuristique basique car il n'est absolument pas nécessaire de passer autant de temps sur ce coup
    """
    # On joue en premier, on renvoie juste une pièce au hasard
    if piece_a_placer is None:
        return 0, Move(None, randrange(0, 15))
    
    # Sinon, on place la pièce donnée à un endroit stratégique (de préférence un coin libre)
    case_choisie = 0
    while plateau.recuperer_piece_1D(case_choisie) is not None:
        case_choisie = choice([0, 15, 12, 3])

    # Pour la pièce à donner, on choisit celle avec le moins de caractéristique en commun par rapport à la pièce à placer (pour éviter de ce mettre dans une situation risquée)
    min_piece_score = 100
    min_piece_id = 0
    for piece_id, piece in list(pioche.items()):
        score = nombre_caracteristiques_communes([piece, piece_a_placer])
        if score < min_piece_score:
            min_piece_score = score
            min_piece_id = piece_id


    return 0, Move(case_choisie, min_piece_id)

def sort_move(move: tuple, plateau: Plateau, pioche: dict, coup_prioritaire: Move) -> int:
    # On joue le coup prioritaire en premier
    if coup_prioritaire is not None and move[0] == coup_prioritaire.place and move[1] == coup_prioritaire.piece_idx:
        return -99999999
    
    # Puis les coups dans l'history heuristic
    coup_id = move[0] * 16 + move[1]
    return -history[coup_id]

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

        moves = generer_coups_legaux(plateau, pioche)
        moves.sort(key= lambda move: sort_move(move, plateau, pioche, coup_prioritaire))

        if maximise:
            max_eval = -200000
            for move in moves:
                case = move[0]
                piece_id = move[1]
                piece = move[2]

                plateau.placer_piece_1D(case, piece)

                if plateau.verifier_alignements():
                    plateau.placer_piece_1D(case, None)
                    return SCORE_VICTOIRE + max_depth, Move(case, None) # le fait d'ajouter max_depth permet de s'assurer que minmax préferera un coup qui mène rapidement à la victoire plutôt qu'on coup qui mène doucement à la victoire
                    
                if not pioche: # Match nul
                    plateau.placer_piece_1D(case, None)
                    return 0, Move(case, None) # 0: score nul parfait

                del pioche[piece_id]
                hash_sauvegarde = list(zb.hash_actuels)
                piece_en_main_sauvegarde = zb.piece_en_main
                zb.jouer_coup(case, piece_id)

                try:
                    f_score, _ = minimax(plateau, pioche, piece, (max_depth - 1), f_eval, max(alpha, max_eval), beta, zb, t_start, t_max, maximise=False)

                    if f_score > max_eval:
                        max_eval = f_score
                        meilleur_coup = Move(case, piece_id)

                        if max_eval >= beta:
                            update_history(case, piece_id, 100)
                            plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué
                            return max_eval, meilleur_coup
                finally:
                    pioche[piece_id] = piece # backtracking, on annule la pièce qu'on avait choisit
                            
                    zb.hash_actuels = hash_sauvegarde
                    zb.piece_en_main = piece_en_main_sauvegarde
                    plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué

            transposition_table[zb.get_canonical_hash()] = {"profondeur": max_depth, "score": max_eval, "move": meilleur_coup}
            return max_eval, meilleur_coup
        else:
            min_eval = 200000


            for move in moves:
                case = move[0]
                piece_id = move[1]
                piece = move[2]

                plateau.placer_piece_1D(case, piece)

                if plateau.verifier_alignements():
                    plateau.placer_piece_1D(case, None)
                    return -SCORE_VICTOIRE - max_depth, Move(case, None) # le fait d'ajouter max_depth permet de s'assurer que minmax préferera un coup qui mène rapidement à la victoire plutôt qu'on coup qui mène doucement à la victoire
                    
                if not pioche: # Match nul
                    plateau.placer_piece_1D(case, None)
                    return 0, Move(case, None) # 0: score nul parfait

                del pioche[piece_id]
                hash_sauvegarde = list(zb.hash_actuels)
                piece_en_main_sauvegarde = zb.piece_en_main
                zb.jouer_coup(case, piece_id)

                try:
                    f_score, _ = minimax(plateau, pioche, piece, (max_depth - 1), f_eval, alpha, min(beta, min_eval), zb, t_start, t_max, maximise=True)

                    if f_score < min_eval:
                        min_eval = f_score
                        meilleur_coup = Move(case, piece_id)

                        if min_eval <= alpha:
                            update_history(case, piece_id, 100)
                            plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué
                            return min_eval, meilleur_coup
                finally:
                    pioche[piece_id] = piece # backtracking, on annule la pièce qu'on avait choisit
                            
                    zb.hash_actuels = hash_sauvegarde
                    zb.piece_en_main = piece_en_main_sauvegarde
                    plateau.placer_piece_1D(case, None) # Backtracking on annule le coup qu'on avait joué

            transposition_table[zb.get_canonical_hash()] = {"profondeur": max_depth, "score": min_eval, "move": meilleur_coup}
            return min_eval, meilleur_coup

def generer_coups_legaux(plateau: Plateau, pioche: dict):
    out = []

    for case in plateau.recuperer_cases_vides():
        for piece_id, piece in list(pioche.items()):
            out.append((case, piece_id, piece))

    return out

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