#Importations
from plateau import *
from Tree import *
from random import choice, shuffle

def selection(node:Node_MCTS, c, state):
    "Phase de sélection"
    while node.get_enfants_directs() != [] and (node.get_untried_moves() is not None and node.get_untried_moves() == []):
        node = max(node.get_enfants_directs(), key=lambda v: v.get_ucb(c))

        move:Move = node.get_move()
        piece_id, case = move.get_piece_idx(), move.get_place()

        state.plateau.placer_piece_1D(case, state.piece_a_jouer)
        state.piece_a_jouer = state.pioche.pop(piece_id)
    return node

def expansion(node:Node_MCTS, state: RootState):
    "Phase d'Expansion"
    if node.get_untried_moves() is None:
        cases = state.plateau.recuperer_cases_vides()
        pieces = list(state.pioche.keys())

        node.gen_untried_moves(cases, pieces)
        shuffle(node.get_untried_moves())

    if not node.get_untried_moves():
        return node

    coup: Move = node.get_untried_moves().pop()
    piece_id, case = coup.get_piece_idx(), coup.get_place()

    piece_a_jouer = state.piece_a_jouer

    state.plateau.placer_piece_1D(case, piece_a_jouer)
    piece_suivante = state.pioche.pop(piece_id)
    state.piece_a_jouer = piece_suivante

    nouvel_enfant = Node_MCTS(coup, node)
    node.insert(nouvel_enfant)

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
                safe_pieces_list += [piece]
            else:
                dangerous_pieces_list += [piece]

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

def backpropagate(node:Node_MCTS, result):
    "Backpropagation"
    while node!=None: #On remonte dans l'arbre et actualise les valeurs des noeuds
        node.increase_visit_number()
        node.increase_win_number(result)
        result = 1 - result
        node = node.get_parent()

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

    if root.enfants: #Si on peut effectuer une action
        best_child = max(root.enfants, key=lambda n: n.win / n.visited if n.visited > 0 else float('-inf'))
        best_move = [best_child.move]
        best_score = [best_child.win / best_child.visited if best_child.visited > 0 else 0]
    else:
        cases = root_state.plateau.recuperer_cases_vides()
        pieces = list(root_state.pioche.keys())
        if cases and pieces: #S'il reste des cases libres et des pièces à donner
            best_move = [Move(choice(cases), choice(pieces))]
            best_score = [0]
        else:
            best_move = [Move(None, None)]
            best_score = [0]
    return best_score, best_move