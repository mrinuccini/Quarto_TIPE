from toolbox import *

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


l = [5,6,4,1,5,6,3]
l_out = n_max(l, 3)
print(l_out)