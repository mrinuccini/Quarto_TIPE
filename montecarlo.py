#Importations
from plateau import *
from Tree import *
from random import choice, shuffle

def remplir_safe_and_dangerous_lists(state):
    """Renvoie les pièces sûres et dangereuses après avoir placé la pièce courante.
     Paramètres :
        state : état du jeu après placement de la pièce courante
    Renvoie :
        safe_pieces_list, dangerous_pieces_list
      """
    safe_pieces_list = []
    dangerous_pieces_list = []

    for piece_id, piece in state.pioche.items():
        safe = True
        for c in state.plateau.recuperer_cases_vides():
            state.plateau.placer_piece_1D(c, piece)
            if state.plateau.verifier_alignements():  # Si l'adversaire peut gagner immédiatement
                safe = False
            state.plateau.placer_piece_1D(c, None)
            if not safe:
                break

        if safe:
            safe_pieces_list.append(piece_id)
        else:
            dangerous_pieces_list.append(piece_id)

    return safe_pieces_list, dangerous_pieces_list


def selection(node:Node_MCTS, c, state):
    """Phase de sélection, on sélectionne des enfants
    Renvoie le meilleur enfant
    """
    while node.get_enfants_directs() != [] and (node.get_untried_moves() is not None and node.get_untried_moves() == []):
        #Tant qu'on n'est pas sur une feuille
        node = max(node.get_enfants_directs(), key=lambda v: v.get_ucb(c)) #On sélectionne le meilleur enfant selon ucb

        move:Move = node.get_move() #On obtient le Move associé
        piece_id, case = move.get_piece_idx(), move.get_place()

        #On joue le coup
        state.plateau.placer_piece_1D(case, state.piece_a_jouer)
        state.piece_a_jouer = state.pioche.pop(piece_id)
    return node #On renvoie le meilleur enfant

def expansion(node:Node_MCTS, state: RootState):
    """Phase d'Expansion, on descend dans l'arbre.
        Crée un nouvel enfant correspondant à un coup non essayé.
    """

    # Génération des mouvements non essayés associés au noeud
    if node.get_untried_moves() is None:
        cases = state.plateau.recuperer_cases_vides()
        pieces = list(state.pioche.keys())
        node.gen_untried_moves(cases, pieces)
        shuffle(node.get_untried_moves())

    if not node.get_untried_moves():
        return node

    # On récupère un Move non essayé
    coup: Move = node.get_untried_moves().pop()
    piece_id, case = coup.get_piece_idx(), coup.get_place()
    piece_a_jouer = state.piece_a_jouer

    # On joue le coup
    state.plateau.placer_piece_1D(case, piece_a_jouer)
    piece_suivante = state.pioche.pop(piece_id)
    state.piece_a_jouer = piece_suivante

    # Création de l'enfant
    nouvel_enfant = Node_MCTS(coup, node)
    node.insert(nouvel_enfant)

    return nouvel_enfant

def simulation(state:RootState):
    """Phase de simulation, on simule une partie au hasard
        Renvoie : 1 si le joueur 1 gagne, 0 si le joueur 2 gagne, 0.5 si nul
    """
    player_turn = 1  # Joueur 2 va jouer (après le coup du joueur 1 à la racine)
    player_turn = 2

    while not state.plateau.verifier_alignements():
        cases = state.plateau.recuperer_cases_vides()
        if not cases:
            return 0.5  # Nul

        # On choisit le meilleur coup possible (maximal safe pieces for next player)
        best_cases = []
        best_safe_piece_count = -1
        for c in cases:
            state.plateau.placer_piece_1D(c, state.piece_a_jouer)
            if not state.plateau.verifier_alignements():
                safe_piece_ids, _ = remplir_safe_and_dangerous_lists(state)
                score = len(safe_piece_ids)
                if score > best_safe_piece_count:
                    best_safe_piece_count = score
                    best_cases = [c]
                elif score == best_safe_piece_count:
                    best_cases.append(c)
            else:
                state.plateau.placer_piece_1D(c, None)
                # Ce coup crée un alignement pour le joueur courant
                return 0 if player_turn == 2 else 1
            state.plateau.placer_piece_1D(c, None)

        if best_cases:
            case = choice(best_cases)
        else:
            case = choice(cases)

        state.plateau.placer_piece_1D(case, state.piece_a_jouer)
        safe_pieces_list, dangerous_pieces_list = remplir_safe_and_dangerous_lists(state)

        piece_id_choisie = None
        if safe_pieces_list:
            piece_id_choisie = choice(safe_pieces_list)
        elif dangerous_pieces_list:
            piece_id_choisie = choice(dangerous_pieces_list)

        if piece_id_choisie is not None:
            state.piece_a_jouer = state.pioche.pop(piece_id_choisie)

        player_turn = 1 if player_turn == 2 else 2

    # Quelqu'un a gagné
    winner = 1 if player_turn == 2 else 2
    return 1 if winner == 1 else 0

def backpropagate(node:Node_MCTS, result):
    "Backpropagation, on applique les changements aux noeuds"
    while node!=None: #On remonte dans l'arbre et actualise les valeurs des noeuds
        node.increase_visit_number()
        node.increase_win_number(result)
        result = 1 - result
        node = node.get_parent()

def mcts(root_state:RootState, c, n_simul):
    "Algorithme de Monte Carlo"
    root = Node_MCTS(None, None)

    for place in root_state.plateau.recuperer_cases_vides():
        root_state.plateau.placer_piece_1D(place, root_state.piece_a_jouer)
        if root_state.plateau.verifier_alignements():
            pieces = list(root_state.pioche.keys())
            root_state.plateau.placer_piece_1D(place, None)
            return [1.0], [Move(place, pieces[0])]
        root_state.plateau.placer_piece_1D(place, None)

    for _ in range(n_simul):
        # Save state before expansion
        state_backup = root_state.cloner()

        node = selection(root, c, state_backup) #On sélectionne le meilleur enfant

        node = expansion(node, state_backup)

        res = simulation(state_backup)

        backpropagate(node, res)

    if root.enfants != []: #Si on peut effectuer une action
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