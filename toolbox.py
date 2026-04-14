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