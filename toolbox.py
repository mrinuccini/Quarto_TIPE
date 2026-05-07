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


def push_insert(l, e ,i):
    """Pousse e dans l à la position i en faisant reculer les éléments derrière"""
    assert(type(l)==list and l!=[])
    assert(type(i)==int and i>=0)

    n = len(l)
    for k in range(0, n-i):
        l[n-k-1] = l[n-k-2]
    l[i] = e
    return l

def n_max(l, n):
    """ Renvoie les indices des n premières valeurs maximales de l"""
    assert(type(l)==list)
    assert(type(n)==int and n>=0)

    if n == 0:
        return []
    if n>=len(l):
        n = len(l)
    
    #Initialisation
    l_out = [-1]*n

    for i in range(0, len(l)):
        print(l_out)
        e = l[i]
        print(e)

        for j in range(0, n-1):
            found = False
            if l_out[j] == -1:
                push_insert(l_out, i, j)
                found = True
                break              
            elif e >= l[l_out[j]]:
                push_insert(l_out, i, j)
                found = True
                break

            if found:
                break
    
    return l_out