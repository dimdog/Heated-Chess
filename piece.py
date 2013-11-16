from collections import namedtuple
import string
Point = namedtuple('Point','x y')
Move = namedtuple('Move','origin destination piece')
class Board:
  def __init__(self):
    self.board=[[]]
    self.turn = None
    self.in_passing=False
    self.last_move = None
    self.whitelist=None
    self.blacklist=None
    self.black=1
    self.white=0
    self.selected = None

  def setup_board(self):
      self.selected=None
      self.whitelist=[Rook(0,0,self.white,self),Rook(7,0,self.white,self),Knight(1,0,self.white,self),Knight(6,0,self.white,self),Bishop(2,0,self.white,self),Bishop(5,0,self.white,self),Queen(3,0,self.white,self),King(4,0,self.white,self)]#+ pawns
      self.blacklist=[Rook(0,7,self.black,self),Rook(7,7,self.black,self),Knight(1,7,self.black,self),Knight(6,7,self.black,self),Bishop(2,7,self.black,self),Bishop(5,7,self.black,self),Queen(3,7,self.black,self),King(4,7,self.black,self)]#+ pawns
      for i in range(0,8):
          self.whitelist.append(Pawn(i,1,self.white,self))
          self.blacklist.append(Pawn(i,6,self.black,self))
      w, h = 8,8
      combined = self.whitelist
      combined.extend(self.blacklist)
      self.board = [[None] * w for i in range(h)]
      for piece in combined:    
          self.board[piece.location.x][piece.location.y]=piece

  def click(self,clicked, selected,turn): # Click event!
     
      if self.occupied(clicked) and self.selected==None:
          piece = self.get_piece(clicked)
          if piece.color != self.turn:
              return False, None
          self.selected=clicked
          return True, self.selected
      elif self.selected==None:
          return False, None 
      
      piece = self.get_piece(self.selected)
      myking = self.king(self.turn)
      assert myking
      if piece.move(clicked):
          temp_piece = self.board[selected.x][selected.y]
          if self.in_passing:
              switch = 1
              if piece.color==black:
                  switch=-1
              self.board[clicked.x][clicked.y-switch]=None
          self.board[self.selected.x][self.selected.y]=None
          self.board[clicked.x][clicked.y]=piece
          piece.location=clicked
          if not self.safe(myking.location,myking.color):
              self.board[self.selected.x][self.selected.y]=piece
              piece.location=self.selected
              if self.in_passing:
                  self.board[clicked.x][clicked.y-switch]=temp_piece        
              else:
                  self.board[clicked.x][clicked.y]=temp_piece
              return False, None
          last_move=Move(selected,clicked,piece)
          self.selected = None
          return True,None
      return False,None

#################

  def moves(self,locx,locy):
      ret = []
      for x in xrange(1,9):
          for y in xrange(1,9):
              if self.board[locx][locy].move(Point(x,y)):
                  ret.append((x,y))
      return ret

  def other_turn(self):
      if self.turn==white:
          return black
      return white


  def safe(self,destination, color): # checks to see if a destination is under threat from a piece of the opposite color
      for piece in self.get_pieces(color):
          if not isinstance(piece, King):
              if piece.move(destination):
                  return False
      return True

  def get_pieces(self,color=None): #returns a list of all the pieces with no arguments, and all pieces of the opposite color if given a color)
      black = self.black
      self.whitelist = self.blacklist = combined = []
      for row in self.board:
          for piece in row:
              if isinstance(piece, Piece):
                  if color==None:
                      combined.append(piece)
                  else:
                      if piece.color == black:
                          self.blacklist.append(piece)
                      else:
                          self.whitelist.append(piece)

      if color==None:
          return combined
      if color==black:
          return self.whitelist
      else:
          return self.blacklist

  def occupied(self,destination, color=None): # checks to see if destination is occupied and a piece of the opposite color, if nothing is provided, will check for any color
      piece=self.get_piece(destination)
      if piece:
          if color==None:
              return True
          else:
              return piece.color==color
      else:
          return False

  def previous_move(self): #returns a move object containing a piece, destination, and origin.       
      return self.last_move

  def king(self,turn): # this will have its logic replaced with a lookup to a global when we start loading in boards turn by turn, for now, for loop!
      for row in self.board:
          for piece in row:
              if isinstance(piece, King) and piece.color==turn:
                  return piece
      return None


  def get_piece(self, destination, y=None):
    if isinstance(destination,str):
      x = string.uppercase.index(string.capitalize(destination[0])) 
      y = int(destination[1])-1
    else:
      if y:
        x = destination
      else:
        x = destination.x
        y = destination.y

    try:
      return self.board[x][y]
    except IndexError:
      return None

class Piece:
    def __init__(self,x,y,color,Board):
        self.location=Point(x,y)
        self.color=color
        self.Board=Board
    
    def square(self,destination):
        return ((1 <= destination.x <= 8) and (1 <= destination.y <= 8))
    
    def rook_move(self,destination): #this is here as a convienence so queen can call this code too
        if self.location.x-destination.x!=0 and self.location.y-destination.y==0:
            x_step=1
            if self.location.x > destination.x:
                x_step=-1
            for i in xrange(self.location.x+x_step,destination.x,x_step):
                if self.Board.occupied(Point(i,self.location.y)):
                    return False
            return not self.Board.occupied(destination,self.color)
        if self.location.y-destination.y!=0 and self.location.x-destination.x==0:
            y_step=1
            if self.location.y > destination.y:
                y_step=-1
            for i in xrange(self.location.y+y_step,destination.y,y_step):
                if self.Board.occupied(Point(self.location.x,i)):
                    return False
            return not self.Board.occupied(destination,self.color)
        return False


    def bishop_move(self,destination): #this is here as a convienence so queen can call this code too
        if abs(self.location.x-destination.x)==abs(self.location.y-destination.y):
            x_step=1
            if self.location.x > destination.x:
                x_step=-1
            y_step=1
            if self.location.y > destination.y:
                y_step=-1
            for x,y in zip(xrange(self.location.x+x_step,destination.x,x_step),xrange(self.location.y+y_step,destination.y,y_step)):
                if self.Board.occupied(Point(x,y)):
                    return False
            return not self.Board.occupied(destination,self.color)
        return False

    def __str__(self):
        c = "White" if self.color==white else "Black"
        return  "%s %s"%(c, self.__class__)
class Pawn(Piece):
    
    def move(self,destination):
        black = self.Board.black
        white = self.Board.white
        if not self.square(destination):
            return False
        switch = -1
        if self.color==black:
            switch=1

        if self.location.y+switch==destination.y and abs(self.location.x-destination.x)==1: # attacking
            return self.Board.occupied(destination,white==self.color) or self.en_passent(destination,switch)
        elif  self.location.x-destination.x==0: # advancing
            if self.location.y+switch==destination.y:
                return not self.Board.occupied(destination)
            elif self.location.y+(switch*2)==destination.y and ((self.color==white and self.location.y==7) or (self.color==black and self.location.y==2)): # Double advancing
                close_destination = Point(destination.x,destination.y-switch)
                return not (self.Board.occupied(destination) and self.Board.occupied(close_destination))
        
    def en_passent(self,destination,switch):
        self.Board.in_passing = False
        if self.Board.last_move:
            last_move = self.Board.last_move
            in_passing = isinstance(last_move.piece, Pawn) and destination.y-switch==last_move.destination.y and destination.x==last_move.destination.x and destination.y+switch==last_move.origin.y
        return self.Board.in_passing
            

class King(Piece):
    
    def move(self,destination):
        return self.square(destination) and self.close(destination) and not self.Board.occupied(destination,self.color) and self.Board.safe(destination,self.color)
    
    def close(self,destination):
        return abs(self.location.x-destination.x)==1 and abs(self.location.y-destination.y)==1

class Knight(Piece):

    def move(self,destination):
        #this one just has a ton of checks for the multitude of combinations possible
        return self.square(destination) and (not self.Board.occupied(destination,self.color)) and ((abs(self.location.x-destination.x)==2 and abs(self.location.y-destination.y)==1) or  (abs(self.location.x-destination.x)==1 and abs(self.location.y-destination.y)==2)) # need it to check for the other color

class Bishop(Piece):
    
    def move(self,destination):
        return self.square(destination) and self.bishop_move(destination)

class Queen(Piece):

    def move(self,destination):
        return self.square(destination) and (self.bishop_move(destination) or self.rook_move(destination))

class Rook(Piece):

    def move(self,destination):
        return self.square(destination) and self.rook_move(destination)


###################

