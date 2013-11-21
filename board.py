from piece import *
 
class Board:
  def __init__(self):
    self.board=[[]]
    self.turn = None
    self.in_passing=False
    self.last_move = None
    self.black=1
    self.white=0
    self.selected = None

  def add_piece(self,piece, location, color):
      x,y = self.translate(location)
      my_piece = piece(location, color, self)
      self.board[x][y]=my_piece

  def setup_board(self):
      w, h = 8,8
      self.board = [[None] * w for i in range(h)]
      self.selected=None
      #Rooks
      self.add_piece(Rook,"A1",self.white)
      self.add_piece(Rook,"H1",self.white)
      self.add_piece(Rook,"A8",self.black)
      self.add_piece(Rook,"H8",self.black)
      #Knights
      self.add_piece(Knight,"B1",self.white)
      self.add_piece(Knight,"G1",self.white)
      self.add_piece(Knight,"B8",self.black)
      self.add_piece(Knight,"G8",self.black)
      #Bishops
      self.add_piece(Bishop,"C1",self.white)
      self.add_piece(Bishop,"F1",self.white)
      self.add_piece(Bishop,"C8",self.black)
      self.add_piece(Bishop,"F8",self.black)
      #Queens
      self.add_piece(Queen,"D1",self.white)
      self.add_piece(Queen,"D8",self.black)
      #Kings
      self.add_piece(King,"E1",self.white)
      self.add_piece(King,"E8",self.black)
    
  
      for i in range(0,8):
          self.add_piece(Pawn,"%s2"%string.ascii_uppercase[i],self.white)
          self.add_piece(Pawn,"%s7"%string.ascii_uppercase[i],self.black)

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
      pieces = self.get_pieces() 
      for piece in pieces:
        ret[piece.location()] = { 'color' : piece.color, 'moves' : piece.moves() }
      return ret

  def move(self, origin, destination, moves=None): #Called like: move("E2","E4")
      piece = self.get_piece(origin)
      if not piece:
        return False, "No piece to move!"
      if self.turn == piece.color:
        return False, "Not your turn!"
      if not moves:
        moves = self.moves()
      if destination in moves[origin]['moves']:
        dest_x,dest_y = self.translate(destination)
        self.board[piece.x][piece.y] = None
        self.board[dest_x][dest_y] = piece
      return True

  def other_turn(self):
      if self.turn==self.white:
          return self.black
      return self.white


  def safe(self,destination, color): # checks to see if a destination is under threat from a piece of the opposite color
      for piece in self.get_pieces(color):
          if not isinstance(piece, King):
              if piece.move(destination):
                  return False
      return True

  def get_pieces(self,color=None): #returns a list of all the pieces with no arguments, and all pieces of the color if given a color)
      print "Get pieces... %s"%color
      white = self.white
      whitelist = blacklist = combined = []
      for row in self.board:
          for piece in row:
              if isinstance(piece, Piece):
                  print "color is: %s"%color
                  if color==None:
                      combined.append(piece)
                      print "None..."
                  else:
                      if piece.color == white:
                          print "white"
                          whitelist.append(piece)
                      else:
                          print "black"
                          blacklist.append(piece)

      if color==None:
          return combined
      elif color==white:
          return whitelist
      else:
          return blacklist

  def occupied(self,x,y, color=None): # checks to see if destination is occupied and a piece of the opposite color, if nothing is provided, will check for any color
      piece=self.get_piece(x,y)
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
    if y or y==0:
      return "%s%d"%(string.ascii_uppercase[code], y+1) 
    return string.uppercase.index(string.capitalize(code[0])), int(code[1])-1
      

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
        


