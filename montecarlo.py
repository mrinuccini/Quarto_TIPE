#Importations
from plateau import *
from Tree import *
from random import choice, shuffle

def remplir_safe_and_dangerous_lists(state, cases):
    """ Renvoie les pièces que l'on peut jouer et celle qu'il ne faut pas jouer
     Paramètres :
        state : état du jeu
         cases : ensemble des cases possibles
    Renvoie :
        safe_pieces_list, dangerous_pieces_list
      """
    safe_pieces_list = []
    dangerous_pieces_list = []

    for piece in state.pioche.keys():
            safe = True
            for c in cases:
                state.plateau.placer_piece_1D(c, state.pioche[piece])
                if state.plateau.verifier_alignements(): #Si on peut perdre on donnant cette pièce
                    safe = False
                
                state.plateau.placer_piece_1D(c, None) #On annule le coup joué

                if not safe:
                    break

            if safe:
                safe_pieces_list += [piece]
            else:
                dangerous_pieces_list += [piece]
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
    """Phase d'Expansion, on descend dans l'arbre
        Renvoie un noeud enfant
    """

    #Génération des mouvements non essayés associé au noeud
    if node.get_untried_moves() is None:
        cases = state.plateau.recuperer_cases_vides()
        pieces = list(state.pioche.keys())
        node.gen_untried_moves(cases, pieces)
        shuffle(node.get_untried_moves())

    if not node.get_untried_moves():
        return node

    #On récupère un Move non essayé
    coup: Move = node.get_untried_moves().pop()
    piece_id, case = coup.get_piece_idx(), coup.get_place()
    piece_a_jouer = state.piece_a_jouer

    #On joue le coup
    state.plateau.placer_piece_1D(case, piece_a_jouer) #On place la pièce sur le plateau
    piece_suivante = state.pioche.pop(piece_id)
    state.piece_a_jouer = piece_suivante

    #Création de l'enfant
    nouvel_enfant = Node_MCTS(coup, node)
    node.insert(nouvel_enfant)

    return nouvel_enfant

def simulation(state:RootState):
    """Phase de simulation, on simule une partie au hasard
        Renvoie : 1 si on gagne, 0 si on perd, 0.5 si nul
    """

    tours_joues = 0
    while not state.plateau.verifier_alignements():    #Tant qu'on n'a pas gagné
        cases = state.plateau.recuperer_cases_vides()
        if not cases:  # Si pas de case disponible
            return 0.5

        case = None

        #On vérifie si un coup nous fait gagner ou perdre à coup sûr
        for c in cases: #Pour chaque case possible, on joue le coup
            state.plateau.placer_piece_1D(c, state.piece_a_jouer)
            if state.plateau.verifier_alignements(): #Si victoire
                state.plateau.placer_piece_1D(c, None)
                return 1 if tours_joues % 2 == 0 else 0 #Renvoie 1 si on gagne, 0 si on perd
            state.plateau.placer_piece_1D(c, None) #On annule le coup joué

        case = choice(cases)

        safe_pieces_list, dangerous_pieces_list = remplir_safe_and_dangerous_lists(state, cases)

        #On choisit une pièce safe si on peut
        piece_id_choisie = None
        if safe_pieces_list != []:
            piece_id_choisie = choice(safe_pieces_list) 
        else:
            if dangerous_pieces_list != []:
                piece_id_choisie = choice(dangerous_pieces_list)

        state.plateau.placer_piece_1D(case, state.piece_a_jouer)
        if piece_id_choisie is not None: state.piece_a_jouer = state.pioche.pop(piece_id_choisie)

        tours_joues += 1

    return 1 if tours_joues % 2 == 0 else 0 #Renvoie si on gagne ou perd selon dernier joueur à avoir joué

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