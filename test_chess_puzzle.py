import pytest
from chess_puzzle import *

#1. test case for location2index
def test_location2index1():
    assert location2index("e2") == (5,2)
def test_location2index2():
    assert location2index("e4") == (5,4)
def test_location2index3():
    assert location2index("a1") == (1,1)
def test_location2index4():
    assert location2index("e5") ==(5,5)
def test_location2index5():
    assert location2index("c3") ==(3,3)
def test_location2index1():
    assert location2index("z3") ==(26,3)

#2. test case for index2location

def test_index2location1():
    assert index2location(5,2) == "e2"
def test_index2location2():
    assert index2location(3,7) == "c7"
def test_index2location3():
    assert index2location(1,1) == "a1"
def test_index2location4():
    assert index2location(8,5) == "h5"
def test_index2location5():
    assert index2location(4,4) == "d4"
def test_index2location6():
    assert index2location(6,3) == "f3"

#Test case for piece class

wq1 = Queen(4,4,True)
wk1 = King(3,5,True)
wq2 = Queen(3,1,True)
bq1 = Queen(5,3,False)
bk1 = King(2,3,False)


B1 = (5, [wq1, wk1, wq2, bq1, bk1])

"""
  ♔  
   ♕ 
 ♚  ♛
     
  ♕  
"""

#4. test case for test_is_piece_at1

def test_is_piece_at1():
    assert is_piece_at(3,2, B1) == False
def test_is_piece_at2():
    assert is_piece_at(17,1, B1) == False
def test_is_piece_at3():
    assert is_piece_at(1,17, B1) == False
def test_is_piece_at4():
    assert is_piece_at(3,1,B1) == True
def test_is_piece_at5():
    assert is_piece_at(4,4,B1) == True

#5. test case for piece_at -King -Queen
def test_piece_at1():
    assert piece_at(4,5, B1) == None
def test_piece_at2():
    assert piece_at(5,3, B1) == bq1
def test_piece_at3():
    assert piece_at(4,4, B1) == wq1
def test_piece_at4():
    assert piece_at(1,1, B1) == None 
def test_piece_at5():  
    assert piece_at(3,5, B1) == wk1

#6. test case for can_reach
def test_can_reach1():
    assert wq1.can_reach(5,4, B1) == True
def test_can_reach2():
    assert wk1.can_reach(4,6, B1) == False
def test_can_reach3():
    assert wq2.can_reach(1,5, B1) == False
def test_can_reach4():
    assert bq1.can_reach(3,5, B1) == False
def test_can_reach5():
    assert bk1.can_reach(1,2, B1) == True

#7. test case for can_move_to
def test_can_move_to1():
    assert wq2.can_move_to(3, 4, B1) == True
def test_can_move_to2():
    assert wk1.can_move_to(5, 4, B1) == False
def test_can_move_to3():
    assert bq1.can_move_to(4, 3, B1) == True
def test_can_move_to4():
    assert bk1.can_move_to(2, 4, B1) == False
def test_can_move_to5():
    assert wq1.can_move_to(5,4, B1) == True

#8. test case for test_move_to1 -- Test1
def test_move_to1():
    wk1a = King(4,5, True)
    Actual_B = wk1.move_to(4,5, B1)
    Expected_B = (5, [wq1, wk1a, wq2, bq1, bk1])
    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_X == piece.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found
        #test 8.2
def test_move_to2():
    wq2a = Queen(3,4, True)
    Actual_B = wq2.move_to(3,4, B1)
    Expected_B = (5, [wq1, wk1, wq2a, bq1, bk1])
    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_X == piece.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found
        #test 8.3
def test_move_to3():
    bq1a = Queen(4,3, False)
    Actual_B = bq1.move_to(4,3, B1)
    Expected_B = (5, [wq1, wk1, wq2, bq1a, bk1])
    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5
    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_X == piece.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found
    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found
         #test 8.4
def test_move_to4():
    bk1a = King(1,3, False)
    Actual_B = bk1.move_to(1,3, B1)
    Expected_B = (5, [wq1, wk1, wq2, bq1, bk1a])
    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5
    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_X == piece.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert  found
    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

#9. test case for test_move_to1 -- Test1
def test_is_check1():
    B2 = (5, [wk1, wq2, bq1, bk1])
    assert is_check(True, B2) == True
def test_is_check2():
    B2 = (5, [wq1, wk1, wq2, bq1, bk1])
    assert is_check(False, B2) == False
def test_is_check3():
    B2 = (5, [wq1, wk1, bq1, bk1])
    assert is_check(False, B2) == False
def test_is_check4():
    wq1 = Queen(3,3,True)
    B2 = (5, [wk1, wq2, bq1, bk1, wq1])
    assert is_check(True, B2) == True
def test_is_check5():
    wq2 = Queen(3,1,False)
    B2 = (5, [wk1, wq2, bq1, bk1])
    assert is_check(True, B2) == True



#10. test case for is_checkmate
def test_is_checkmate1():
    B2 = (5, [wk1, wq2, bq1, bk1])
    assert is_checkmate(True, B2) == False

def test_is_checkmate2():
    B2 = (5, [wq1, wk1, wq2, bq1, bk1])
    assert is_checkmate(False, B2) == False

def test_is_checkmate3():
    wk1 = King(3,5,True)
    wq2 = Queen(3,1,True)
    bq1 = Queen(5,3,False)
    bk1 = King(1,5,False)
    B2 = (5, [wq1, wk1, wq2, bq1, bk1])
    assert is_checkmate(False, B2) == False
#11. test for  board_read test1
def test_read_board1():
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


def test_conf2unicode1():
    assert conf2unicode(B1).rstrip("\n") == "  ♔  \n   ♕ \n ♚  ♛\n     \n  ♕  "