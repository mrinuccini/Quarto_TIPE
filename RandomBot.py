from piece import *
from plateau import *
from Algo import Algorithm
import random

class RandomBot(Algorithm):
    """
        Algorithme jouant complètement au hasard
    """

    def choisir_piece(self, plateau, pioche):
        return random.randrange(0, len(pioche))

    def choisir_place(self, plateau, pioche, piece):
        return random.randrange(0, len(plateau.recuperer_cases_vides()))