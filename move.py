class Move:
    "Coup lors d'un tour"
    def __init__(self, place:int, piece_idx:int):
        """ Paramètres :
                place : int, position où on va placer la pièce en cours
                piece_idx : int, indice de la pièce à donner à l'adversaire
        """
        self.place = place
        self.piece_idx = piece_idx

    def get_place(self):
        "Renvoie où placer la pièce"
        return self.place
    
    def get_piece_idx(self):
        "Renvoie l'indice de la pièce à jouer pour l'autre joueur"
        return self.piece_idx