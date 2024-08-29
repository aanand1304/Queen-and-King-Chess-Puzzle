from typing import Tuple, List
from copy import deepcopy
import random

def location2index(loc: str) -> Tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    column = loc[0]
    rowPosition = int(loc[1:])
    columnPosition = ord(column) - ord('a') + 1
    return columnPosition, rowPosition

def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    columnChar= chr(ord('a')+x-1)
    rowPosition =y
    # print(columnChar,y)
    return f"{columnChar}{rowPosition}"

class Piece:
  pos_x : int	
  pos_y : int
  side : bool #True for White and False for Black
  def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
    '''sets initial values'''
    self.pos_X =pos_X
    self.pos_Y =pos_Y
    self.side = side_


Board = Tuple[int, List[Piece]]
def is_piece_at(pos_X: int, pos_Y: int, B: Board) -> bool:
    '''checks if there is a piece at coordinates pos_X, pos_Y of board B''' 
    size, pieces = B
    for piece in pieces:
        if piece.pos_X == pos_X and piece.pos_Y == pos_Y:
            #print("::::::is_piece_at::::",piece.pos_X,piece.pos_Y)
            return True
    return False

def piece_at(pos_X: int, pos_Y: int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pos_X, pos_Y of board B 
    assumes some piece at coordinates pos_X, pos_Y of board B is present
    '''
    size, pieces = B
    for piece in pieces:
        if piece.pos_X == pos_X and piece.pos_Y == pos_Y:
            return piece
    return None

#queen class

class Queen(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)
	
    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
      '''
      checks if this queen can move to coordinates pos_X, pos_Y
      on board B according to rule [Rule1] and [Rule3] (see section Intro)
      Hint: use is_piece_at
     '''
      #print("Queen Can_reach")
      board_Size, pieces = B
      if not (1 <= pos_X <= board_Size and 1 <= pos_Y <= board_Size):return False
      if pos_X == self.pos_X and pos_Y == self.pos_Y:
        return False
      if not is_piece_at(pos_X, pos_Y, B) or piece_at(pos_X, pos_Y, B).side != self.side :
        if pos_X == self.pos_X or pos_Y == self.pos_Y or abs(pos_X - self.pos_X) == abs(pos_Y - self.pos_Y):
            step_X = 1 if pos_X > self.pos_X else -1 if pos_X < self.pos_X else 0
            step_Y = 1 if pos_Y > self.pos_Y else -1 if pos_Y < self.pos_Y else 0
            new_pos_X, new_pos_Y = self.pos_X + step_X, self.pos_Y + step_Y
            while new_pos_X != pos_X or new_pos_Y != pos_Y:
                if is_piece_at(new_pos_X, new_pos_Y, B): 
                    return False
                new_pos_X += step_X
                new_pos_Y += step_Y
            return True
        return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''
        checks if this queen can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - done firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if the result of the move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - done thirdly, construct a new board resulting from the move
        - finally, to check [Rule4], use is_check on the new board
        '''
        if not self.can_reach(pos_X, pos_Y, B):
            return False
        capture_piece= None
        if is_piece_at(pos_X, pos_Y, B):
          capture_piece = piece_at(pos_X, pos_Y, B)       
        new_board = self.move_to(pos_X, pos_Y, B)
        if is_check(self.side, new_board):
            #print("HI Check is therer")
            return False
        
        if capture_piece is None:
            return True
        
        return True

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        '''
        returns a new board resulting from the move of this queen to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        size, pieces = B
        new_pieces = []
        for piece in pieces:
            if (piece.pos_X == pos_X and piece.pos_Y == pos_Y):
                continue
            elif piece.pos_X == self.pos_X and piece.pos_Y == self.pos_Y:
                new_pieces.append(Queen(pos_X, pos_Y, piece.side))
            else:
                new_pieces.append(piece)
        return size, new_pieces

#  King class-----
class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X,pos_Y,side_)
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]'''
        board_size, pieces = B
        if not (1 <= pos_X <= board_size and 1 <= pos_Y <= board_size):return False
        if pos_X == self.pos_X and pos_Y == self.pos_Y:
            return False
        if is_piece_at(pos_X, pos_Y, B) and piece_at(pos_X, pos_Y, B).side == self.side: 
            return False
        if abs(pos_X - self.pos_X) <= 1 and abs(pos_Y - self.pos_Y) <= 1:
            return True
        return False
    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
      '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
      board_size, pieces = B
      if not self.can_reach(pos_X, pos_Y, B):
          return False
      for piece in pieces:
          if isinstance(piece, Queen) and piece.side != self.side:
              if piece.can_reach(pos_X, pos_Y, B):
                  start_X, start_Y = self.pos_X, self.pos_Y
                  if not piece.can_reach(start_X, start_Y, B) or not piece.can_reach(pos_X, pos_Y, B):
                      return False
      capture_piece = None
      if is_piece_at(pos_X, pos_Y, B):
          capture_piece = piece_at(pos_X, pos_Y, B)

      new_board = self.move_to(pos_X, pos_Y, B)

      if is_check(self.side, new_board):
          return False

      if capture_piece is None:
          return True

      return True

    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        #print("I am king classs move_to function")
        size, pieces = B
        new_pieces = []
        for piece in pieces:
            if (piece.pos_X == pos_X and piece.pos_Y == pos_Y):
                continue
            elif piece.pos_X == self.pos_X and piece.pos_Y == self.pos_Y:
                new_pieces.append(King(pos_X, pos_Y, piece.side))
            else:
                new_pieces.append(piece)
        return size, new_pieces

#*****************
def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
    ''' Finding King and checking if anyone can reach to King position'''
    king_Position =None
    board, pieces =B
    for piece in pieces:
        if isinstance(piece, King) and piece.side==side:
            king_Position = (piece.pos_X, piece.pos_Y)
            #print("Is_check",king_Position)
            break
        if king_Position is None:
            return False

    for piece in pieces:
        if piece.side != side:
            if piece.can_reach(king_Position[0],king_Position[1], B):
                return True
              
    return False

def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side
    Hints: 
    - use is_check
    - use can_move_to
    '''
    board_Size, pieces =B
    if not is_check(side, B):
        return False
    for piece in pieces:
        if piece.side == side:
            for row in range(1, board_Size+1):
                for col in range (1, board_Size+1):
                    if piece.can_move_to(row,col,B):
                        new_board= piece.move_to(col,row,B)
                        if not is_check(side, new_board):
                            return False
    return True

def is_stalemate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is stalemate for side

    Hints: 
    - use is_check
    - use can_move_to 
    '''
    if is_check(side, B):
        return False
    board_Size, pieces = B

    for piece in pieces:
        if piece.side == side:
            for x in range (1, board_Size+1):
                for y in range (1, board_Size+1):
                    if not piece.can_move_to(x,y,B):
                        return False

    return True


#This function is helping readboard to create pieces 
def pieceFunc(data:str, isWhiteBlack:bool) -> Piece:
    loc =data.strip()
    column,row = location2index(loc[1:])
    pieceType = loc[0]
    side =isWhiteBlack
    if (pieceType=='K'):
        #print("King",row,column)
        return King(column,row,isWhiteBlack )
    else:
        #print("Queen",row,column)
        return Queen(column,row,isWhiteBlack )

def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''
    try:
        # fileName = filename
        file_read = open(filename,'r')
        pieces = []
        boardSize =int(file_read.readline().strip())
        whiteLocation = file_read.readline().strip().split(",")
        blackLocation=file_read.readline().strip().split(",")
        for loc_w in whiteLocation:
            pieces.append(pieceFunc(loc_w, True))
        for loc_b in blackLocation:
            pieces.append(pieceFunc(loc_b, False))
        return boardSize, pieces
    except FileNotFoundError:
        print(f"The file '{filename}' was not found")
    except Exception as err:
        print(f"The file '{filename}' ", err)
# saving  file
def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
    try:
        boardSize, pieces =B
        currentBoard = deepcopy(B)
        file = open(filename, 'w')
        file.write(str(boardSize)+'\n')
        whiteDetail=[]
        blackDetails =[]
        for piece in pieces:
            if piece.side==True:
                class_name = type(piece).__name__[0]
                pieceLocation = index2location(piece.pos_X,piece.pos_Y)
                whiteDetail.append(class_name+pieceLocation)
            else:
                class_name = type(piece).__name__[0]
                pieceLocation = index2location(piece.pos_X,piece.pos_Y)
                blackDetails.append(class_name+pieceLocation)
        file.write(', '.join(whiteDetail)+ '\n')
        file.write(', '.join(blackDetails)+ '\n')
    except Exception as err:
        print("err")
    finally:
        file.close()

def find_black_move(B: Board) -> Tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''
    board_size,pieces = B
    blackPiece=[piece for piece in pieces if piece.side == False ]
    while True:
        randomBlackPiece =random.choice(blackPiece)
        x_cord = random.randint(1, board_size)
        y_cord = random.randint(1,board_size)
        #print(randomBlackPiece,x_cord,y_cord )
        if randomBlackPiece.can_move_to(x_cord,y_cord, B):
            return randomBlackPiece, x_cord , y_cord


def conf2unicode(B: Board) -> str: 
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''
    unicodePiece = {'W_King':'♔','W_Queen':'♕', 'B_King':'♚', 'B_Queen':'♛'}
    board =[[' '  for _ in range(B[0])]for _ in range(B[0])]
    for piece in B[1]:
        if piece.side==True:
            white_black ='W_'       
        else:
            white_black ='B_'
        
        class_name = type(piece).__name__
        pieceType=white_black+class_name
        symbol = unicodePiece[pieceType]
        #print(piece.pos_X - 1,piece.pos_Y - 1)
        board[piece.pos_Y - 1][piece.pos_X - 1] = symbol
    return '\n'.join([''.join(row) for row in board[::-1]])

#This function is just helping white move to check valid input  
def is_valid_input(move:str,board: Board) -> bool:
    if (len(move)==4):
        white_origin= move[:2]
        white_move=move[2:]
        white_origin_col, white_origin_row =location2index(white_origin)
        white_move_col, white_move_row =location2index(white_move)
        if  (white_origin[0].isalpha() and white_origin[1:].isdigit() and white_move[0].isalpha() and white_move[1:].isdigit()):
            if is_piece_at(white_origin_col,white_origin_row,board):
                return True
    return False

def main()->None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''   
    while True:
        try:
            filename = input("File name for initial configuration: ")
            initialBoard =read_board(filename.lower())
            print(conf2unicode(initialBoard))
            break
        except Exception as err:
            print(" This is not a valid file. File name for initial configuration:")
            

    while True:
        ##White move#
        white_Move = input("Next move of White:")
        if white_Move.lower() == 'quit':
            save_file = input("File name to store the configuration:")
            save_board(save_file,initialBoard)
            print("The game configuration saved.")
            break

        if is_valid_input(white_Move,initialBoard):
            white_origin= white_Move[:2]
            white_move=white_Move[2:]
            white_origin_col, white_origin_row =location2index(white_origin)
            white_move_col, white_move_row =location2index(white_move)
            print(white_origin_col, white_origin_row,white_move_col, white_move_row)
            piece = piece_at(white_origin_col,white_origin_row,initialBoard)
            if( piece.can_move_to(white_move_col, white_move_row, initialBoard)):
                new_board = piece.move_to(white_move_col, white_move_row, initialBoard)
                initialBoard =deepcopy(new_board)
                print("The configuration after White's move is:",conf2unicode(new_board), sep="\n")
                if is_checkmate(False, initialBoard):
                    print("Game over. White wins.")
                    break
                if is_stalemate(False, initialBoard):
                    print("Game over. Stalemate.")
                    break 
            else:
                print("This is not a valid move.",end=" ")
                continue
        else:
            print("This is not a valid move.",end=" ")
            continue
        #print("Finally starting black")
#black move
        black_move = find_black_move(initialBoard)
        black_origX, black_origY = black_move[0].pos_X, black_move[0].pos_Y 
        black_movX, black_movY =black_move[1], black_move[2]
        b_origin =index2location(black_origX,black_origY)
        b_move = index2location(black_movX,black_movY)
        print(f"Next move of black is {b_origin[0]}{b_origin[1]}{b_move[0]}{b_move[1]}.")
        #print(black_movX, black_movY)
        new_board=black_move[0].move_to(black_movX,black_movY, new_board)
        initialBoard = deepcopy(new_board)
        print("The configuration after black's move is:",conf2unicode(new_board), sep="\n")
        if is_checkmate(True,initialBoard):
            print("Game over. Black wins.")
            break
        if is_stalemate(True,initialBoard):
            print("Game over. Stalemate.")
            break

if __name__ == '__main__': #keep athis in
   main()