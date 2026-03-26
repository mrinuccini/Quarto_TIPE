"Instanciation des joueurs"
TYPES = ["Humain", "Monte Carlo", "MinMax"]


class Joueur:
    def __init__(self, typ="Humain", niveau=1):
        """ Paramètre :
                type : chaîne de caractères, élément de TYPES
                       type de joueur
                niveau : entier naturel
                         niveau de l'IA
        """
        assert(typ in TYPES)
        self.type = typ
        self.niveau = niveau

    def choisir_piece(self, plateau, pioche):
        """ Choix d'une pièce que devra placer le joueur suivant, selon le type du joueur """
        pass

    def choisir_place(self, plateau, pioche, piece):
        """ Choix du placement de la pièce selon le type du joueur """
        pass