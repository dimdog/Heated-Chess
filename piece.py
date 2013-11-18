from collections import namedtuple
import string
Move = namedtuple('Move','origin destination piece')

class Piece:
    def __init__(self,x,y,color,Board):
      self.x = x
      self.y = y
      self.color=color
      self.moved = False
      self.Board=Board

    def location(self):
      return "%s%d"%(string.ascii_uppercase[self.x], self.y)
    
    def square(self,destination):
      return ((1 <= destination.x <= 8) and (1 <= destination.y <= 8))
    
    def rook_move(self,destination): #this is here as a convienence so queen can call this code too
      if self.x-destination.x!=0 and self.y-destination.y==0:
        x_step=1
        if self.x > destination.x:
          x_step=-1
        for i in xrange(self.x+x_step,destination.x,x_step):
          if self.Board.occupied(Point(i,self.y)):
            return False
        return not self.Board.occupied(destination,self.color)
      if self.y-destination.y!=0 and self.x-destination.x==0:
        y_step=1
        if self.y > destination.y:
          y_step=-1
        for i in xrange(self.y+y_step,destination.y,y_step):
          if self.Board.occupied(Point(self.x,i)):
            return False
        return not self.Board.occupied(destination,self.color)
      return False


    def bishop_move(self,destination): #this is here as a convienence so queen can call this code too
      if abs(self.x-destination.x)==abs(self.y-destination.y):
        x_step=1
        if self.x > destination.x:
          x_step=-1
        y_step=1
        if self.y > destination.y:
          y_step=-1
        for x,y in zip(xrange(self.x+x_step,destination.x,x_step),xrange(self.y+y_step,destination.y,y_step)):
          if self.Board.occupied(Point(x,y)):
            return False
        return not self.Board.occupied(destination,self.color)
      return False

    def __str__(self):
      c = "W" if self.color==self.Board.white else "B"
      return  "%s%s"%(c, str(self.__class__.__name__)[:2])

class Pawn(Piece):
    
  def moves(self):
    ret = []
    switch = -1
    start = 7
    if self.color==self.Board.white:
      switch = 1
      start = 2
    #normal move
    if not self.Board.occupied(self.x, self.y+switch):
      ret.append(self.Board.translate(self.x, self.y+switch))
      #double move
      if int(self.location()[1])==start:
        if not self.Board.occupied(self.x, self.y+(switch*2)):
          ret.append(self.Board.translate(self.x, self.y+(switch*2)))
      #attack left
      if self.Board.occupied(self.x+1, self.y+switch, self.color):
        ret.append(self.Board.translate(self.x+1, self.y+switch))
      #attack right
      if self.Board.occupied(self.x-1, self.y+switch, self.color):
        ret.append(self.Board.translate(self.x-1, self.y+switch))
      #TODO en passent
            
      
    
  def en_passent(self,destination,switch):
    self.Board.in_passing = False
    if self.Board.last_move:
      last_move = self.Board.last_move
      in_passing = isinstance(last_move.piece, Pawn) and destination.y-switch==last_move.destination.y and destination.x==last_move.destination.x and destination.y+switch==last_move.origin.y
    return self.Board.in_passing
        

class King(Piece):
    
  def moves(self):
    pass

  def move(self,destination):
    return self.square(destination) and self.close(destination) and not self.Board.occupied(destination,self.color) and self.Board.safe(destination,self.color)
  
  def close(self,destination):
    return abs(self.x-destination.x)==1 and abs(self.y-destination.y)==1

class Knight(Piece):
  
  def moves(self):
    pass

  def move(self,destination):
    #this one just has a ton of checks for the multitude of combinations possible
    return self.square(destination) and (not self.Board.occupied(destination,self.color)) and ((abs(self.x-destination.x)==2 and abs(self.y-destination.y)==1) or  (abs(self.x-destination.x)==1 and abs(self.y-destination.y)==2)) # need it to check for the other color

class Bishop(Piece):

  def moves(self):
    pass
    
  def move(self,destination):
    return self.square(destination) and self.bishop_move(destination)

class Queen(Piece):

  def moves(self):
    pass

  def move(self,destination):
    return self.square(destination) and (self.bishop_move(destination) or self.rook_move(destination))

class Rook(Piece):

  def moves(self):
    pass

  def move(self,destination):
    return self.square(destination) and self.rook_move(destination)


###################

