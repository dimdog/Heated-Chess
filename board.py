from piece import *
 
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
          self.board[piece.x][piece.y]=piece

  def click(self,clicked): # Click event!
     
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

  def moves(self):
      ret = {}
      pieces = self.whitelist + self.blacklist
      for piece in pieces:
        ret[piece.location()] = { 'color' : piece.color, 'moves' : piece.moves() }
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
      x,y = self.translate(destination)
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
    
  def translate(self, code, y=None):
    if y:
      return "%s%d"%(string.ascii_uppercase[code], y) 
    return string.uppercase.index(string.capitalize(code[0])), int(code[1])
      

  def __str__(self):
    ret = "|%s|"*8
    ret+="\n"
    ret = ret*8
    ls = []
    for column in xrange(1,9):
      for row in xrange(0,8):
        piece = self.get_piece("%s%d"%(string.ascii_uppercase[row],column))
        if piece:
          ls.append(piece.__str__().ljust(3))
        else:
          ls.append("".ljust(3))
    return ret%tuple(ls)
        


