##Fonctions utiles
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



##Tests
def tests():
    assert(convert_matrice([[]])==[[]])

    M1 = [
        [1,2,3],
        [4,5,6]
    ]
    assert(convert_matrice(M1)==[[1,4], [2,5], [3,6]])
    assert(convert_matrice(convert_matrice(M1))==M1)

    M2 = [
        [1],
        [2],
        [3],
    ]
    assert(convert_matrice(M2)==[[1,2,3]])
    assert(convert_matrice(convert_matrice(M2))==M2)    


tests()