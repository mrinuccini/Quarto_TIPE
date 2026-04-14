from piece import Piece, comp

##Tests
def test():
     p1 = Piece(1,1,1,1)
     p2 = Piece(1,0,1,0)
     p3 = Piece(1,0,0,0)
     p4 = Piece(1,1,0,1)
     p5 = Piece(0,0,0,0)
     assert(comp([p1,p2,p3,p4])==True)
     assert(comp([p1,p5,p3,p4])==False)
     assert(comp([p5,p3,p4])==True)


test()