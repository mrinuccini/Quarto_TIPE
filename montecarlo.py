#Importations
from plateau import *
from Tree import *
from random import choice, shuffle

def selection(node:Node_MCTS, c, state):
    "Phase de Sélection"
    while node.enfants != [] and (node.untried_move is not None and node.untried_move == []):
        node = max(node.enfants, key=lambda v: v.get_ucb(c)) #On cherche la feuille avec la valeur ucb maximale

        move:Move = node.move
        piece_id, case = move.get_piece_idx(), move.get_place()

        state.plateau.placer_piece_1D(case, state.piece_a_jouer)
        state.piece_a_jouer = state.pioche.pop(piece_id)
    return node

def expansion(node:Node_MCTS, state: RootState):
    "Phase d'Expansion"
    if node.untried_move is None:
        cases = state.plateau.recuperer_cases_vides()
        pieces = list(state.pioche.keys())

        node.untried_move = [Move(c, p) for c in cases for p in pieces]
        shuffle(node.untried_move)

    if not node.untried_move:
        return node

    coup: Move = node.untried_move.pop()
    piece_id, case = coup.get_piece_idx(), coup.get_place()

    piece_a_jouer = state.piece_a_jouer

    state.plateau.placer_piece_1D(case, piece_a_jouer)
    piece_suivante = state.pioche.pop(piece_id)
    state.piece_a_jouer = piece_suivante

    nouvel_enfant = Node_MCTS(coup, node)
    node.enfants.append(nouvel_enfant)

    return nouvel_enfant

def simulation(state:RootState):
    "Phase de simulation"

    tours_joues = 0
    while not state.plateau.verifier_alignements():
        cases = state.plateau.recuperer_cases_vides()
        if not cases:  # Si pas de case disponible
            return 0.5

        case = None

        for c in cases:
            state.plateau.placer_piece_1D(c, state.piece_a_jouer)
            if state.plateau.verifier_alignements():
                state.plateau.placer_piece_1D(c, None)
                return 1 if tours_joues % 2 == 0 else 0
            state.plateau.placer_piece_1D(c, None)

        case = choice(cases)

        safe_pieces_list = []
        dangerous_pieces_list = []
        cases = state.plateau.recuperer_cases_vides()

        for piece in list(state.pioche.keys()):
            safe = True
            for c in cases:
                state.plateau.placer_piece_1D(c, state.pioche[piece])
                if state.plateau.verifier_alignements():
                    safe = False
                state.plateau.placer_piece_1D(c, None)

                if not safe:
                    break
            if safe:
                safe_pieces_list.append(piece)
            else:
                dangerous_pieces_list.append(piece)

        piece_id_choisie = None
        if safe_pieces_list:
            piece_id_choisie = choice(safe_pieces_list)
        else:
            if dangerous_pieces_list != []:
                piece_id_choisie = choice(dangerous_pieces_list)

        state.plateau.placer_piece_1D(case, state.piece_a_jouer)
        if piece_id_choisie is not None: state.piece_a_jouer = state.pioche.pop(piece_id_choisie)

        tours_joues += 1

    return 1 if tours_joues % 2 == 0 else 0

def backpropagate(node, result):
    "Backpropagation"
    while node!=None: #On remonte dans l'arbre et actualise les valeurs des noeuds
        node.visited += 1
        node.win += result
        result = 1 - result
        node = node.parent

def mcts(root_state:RootState, c, n_simul):
    "Algorithme de Monte Carlo"
    root = Node_MCTS(None, None)
    for _ in range(n_simul):
        # Save state before expansion
        state_backup = root_state.cloner()

        node = selection(root, c, state_backup)

        node = expansion(node, state_backup)

        res = simulation(state_backup)

        backpropagate(node, res)

    best_move = [max(root.enfants, key=lambda n: n.visited).move]

    best_score = [max(root.enfants, key=lambda n: n.visited).visited]
    return best_score, best_move