#Importations
from plateau import *
from Tree import *
from random import choice

def selection(node:Node_MCTS, c):
    "Phase de Sélection"
    while node.enfants != []:
        node = max(node.enfants, key=lambda v: v.get_ucb(c)) #On cherche la feuille avec la valeur ucb maximale
    return node

def expansion(node:Node_MCTS):
    "Phase d'Expansion"
    cases = node.val.plateau.recuperer_cases_vides() #Cases vides
    pioche = node.val.pioche #pioche

    #Pour chaque possibilité :
    for case in cases:
        for piece_idx in pioche:
            piece_suiv = pioche[piece_idx] #Piece à donner au tour suivant
            nv_plateau = node.val.plateau.cloner() #Plateau clone
            nv_plateau.placer_piece_1D(case, node.val.piece_a_jouer) #On place la pièce

            nv_pioche = node.val.pioche.copy() #Nouvelle pioche
            del nv_pioche[piece_idx] #On retire de la pioche la pièce

            nv_state = RootState(nv_plateau, nv_pioche, piece_suiv) #Nouvel état de jeu

            node.insert(Node_MCTS(nv_state, (piece_idx, case))) #Nouveau noeud que l'on insère

    if node.enfants != []:
        return choice(node.enfants)
    return node

def simulation(state:RootState):
    "Phase de simulation"
    state2 = state.cloner()
    while not state2.plateau.verifier_alignements():
        cases = state2.plateau.recuperer_cases_vides()
        if cases==[]:
            return False
        
        if not state2.pioche:  # Si pioche vide
            return False
        if not cases:  # Si aucune case disponible
            return False
        case = choice(cases)
        piece = choice(list(state2.pioche.keys()))

        nv_plateau = state2.plateau.cloner()
        nv_plateau.placer_piece_1D(case, state2.piece_a_jouer)

        nv_pioche = {key:state2.pioche[key] for key in state2.pioche}
        del nv_pioche[piece]

        state2 = RootState(nv_plateau, nv_pioche, state2.pioche[piece])
    return True

def backpropagate(node, result):
    "Backpropagation"
    while node!=None: #On remonte dans l'arbre et actualise les valeurs des noeuds
        node.visited += 1
        if result == 1:
            node.win += 1
        node = node.parent

def mcts(root_state:RootState, c, n_simul):
    "Algorithme de Monte Carlo"
    root = Node_MCTS(root_state)
    for _ in range(n_simul):
        node = selection(root, c)
        node = expansion(node)
        res = simulation(node.val)
        backpropagate(node, res)
    best_node = max(root.enfants, key=lambda n: n.visited)
    score = best_node.win / best_node.visited
    best_move =  best_node.move
    
    return score, best_move