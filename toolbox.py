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
    if all(e == None for e in pieces):
        return 0
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

        e = l[i]


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


def max_k_v(L_keys, L_values):
    """ Renvoie la clé maximale de L_keys et sa valeur associée dans L_values
        Paramètres :
            L_keys et L_values deux listes de même taille
        Renvoie :
            max_key, max_val
    """
    assert(type(L_keys)==list and type(L_values)==list and len(L_keys)==len(L_values))

    if L_keys == []:
        return
    n = len(L_keys)
    max_key = L_keys[0]
    max_val = L_values[0]
    for i in range(1, n):
        key = L_keys[i]
        val = L_values[i]
        if key>max_key:
            max_key = key
            max_val = val
    return max_key, max_val


def test():
    L1 = [5,6,7,8,9]
    L2 = [7,8,4,5,6]
    print(max_k_v(L1, L2))