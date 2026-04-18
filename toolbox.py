"""Ensembles de fonctions utiles
convert_matrice(M)
"""


def convert_matrice(M):
    """ Intervertit les lignes et les colonnes de la matrice M """
    #Assertions
    assert(type(M)==list)
    assert(M!=[])
    assert(type(M[0])==list)

    #Matrice vide
    if M==[[]]:
        return [[]]
    
    n = len(M)
    p = len(M[0])
    M2 = []

    for j in range(p):
        line = []
        for i in range(n):
            line += [M[i][j]]
        M2 += [line]
    return M2

def nombre_caracteristiques_communes(pieces: list) -> int:
    """
    Renvoie le nombre de caractéristiques communes qu'on une liste de pièce
    """
    assert(L!=[])
    assert(type(L)==list)

    if len(pieces) == 0: 
        return 0

    count = 0
    
    if all(p.couleur == pieces[0].couleur for p in pieces[1:]):
        count += 1
    if all(p.forme == pieces[0].forme for p in pieces[1:]):
        count += 1
    if all(p.dessus == pieces[0].dessus for p in pieces[1:]):
        count += 1
    if all(p.taille == pieces[0].taille for p in pieces[1:]):
        count += 1
    
    return count