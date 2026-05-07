from montecarlo import *
from minmax import *

def xterminator(root_state:RootState, c, n_simul, n_res, max_depht):
    """ Algorithme qui mélange MinMax et MonteCarlo : on sélectionne n_res noeuds avec mcts et pour chacun on effectue MinMax
            Paramètres :
                - c : float, coefficient d'exploration de mcts
                - n_simul : entier naturelnon nul, nombre de simulations avec mcts
                - n_res : entier naturel non nul, nombre de résultats avec mcts
                - max_depht : entier naturel non nul, profondeur maximale atteinte par MinMax
    """
    #Assertions
    assert(type(c)==float)
    assert(type(n_simul)==int and n_simul > 0)
    assert(type(n_res)==int and n_res > 0)
    assert(type(max_depht)==int and max_depht > 0)

    #On récupère les n_res meilleurs positions selon mcts
    scores_mcts, moves = mcts(root_state, c, n_simul, n_res)

    state = root_state.cloner()
    scores = []
    best_moves = []

    for move in moves: #Pour chaque positions choisies
        state = root_state.cloner()

        piece_idx, place  = move.get_piece_idx(), move.get_place()
        plateau = state.plateau
        pioche = state.pioche
        piece = state.piece_a_jouer


        #On place la pièce sur le plateau
        plateau.placer_piece_1D(place, piece)

        
        piece_suiv = pioche[piece_idx]
        del pioche[piece_idx]

        #On lance MinMax sur cette position
        score, _ = minimax(plateau, pioche, piece_suiv, max_depht, evaluate1, float("-inf"), float("inf"), maximise=True)

        #On récupère les résultats
        scores += [score]
        best_moves += [move]

    score, best_move = max_k_v(scores, best_moves)
    return score, best_move