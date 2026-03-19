def convert_matrice(M):
    assert(type(M)==list)
    assert(M!=[])
    assert(type(M[0])==list)

    n = len(M)
    p = len(M[0])
    M2 = []

    for j in range(p):
        line = []
        for i in range(n):
            line += [M[i][j]]
        M2 += [line]
    return M2