from montecarlo import *
from minmax import *

def xterminator(root_state:RootState, c, n_simul, n_res, max_depht):
    scores_mcts, moves = mcts(root_state, c, n_simul, n_res)
    state = root_state.cloner()

    scores = []
    best_moves = []

    for move in moves:
        place, piece_suiv = move
        plateau = state.plateau
        piece = state.piece_a_jouer
        pioche = state.pioche
        plateau.placer_piece_1D(place, piece)
        del pioche[piece]
        score, best_move = minimax(plateau, pioche, piece_suiv, max_depht, evaluate1, float("-inf"), float("inf"), maximise=True)
        scores += [score]
        best_moves += [move]

    score = scores[0]
    best_move = best_moves[0]
    for i in range(len(scores)):
        if scores[i] > score:
            score = scores[i]
            best_move = best_moves[i]
    return score, best_move