"Instanciation des joueurs"
TYPES = ["Humain", "Monte Carlo", "MinMax"]


class Joueur:
    def __init__(self, type="Humain", niveau=1):
        """ Paramètre :
                type : chaîne de caractères, élément de TYPES
                       type de joueur
                niveau : entier naturel
                         niveau de l'IA
        """