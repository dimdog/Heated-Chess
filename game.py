from collections import defaultdict
import pygame, sys, chess
from pygame.locals import *

class ColorTuple(object):
  def __init__(self):
    self.r = 0
    self.g = 20
    self.b = 0

class HeatedChess:
  columns = ["A","B","C","D","E","F","G","H"] 
  rows = [8,7,6,5,4,3,2,1]
  whiteColor = pygame.Color(255,255,255)
  blackColor = pygame.Color(0,0,0)
  #PAWN
  white_pawn = pygame.image.load('pieces/white_pawn.png')
  black_pawn = pygame.image.load('pieces/black_pawn.png')
  #KNIGHT
  white_knight = pygame.image.load('pieces/white_knight.png')
  black_knight = pygame.image.load('pieces/black_knight.png')
  #BISHOP
  white_bishop = pygame.image.load('pieces/white_bishop.png')
  black_bishop = pygame.image.load('pieces/black_bishop.png')
  #ROOK
  white_rook = pygame.image.load('pieces/white_rook.png')
  black_rook = pygame.image.load('pieces/black_rook.png')
  #QUEEN
  white_queen = pygame.image.load('pieces/white_queen.png')
  black_queen = pygame.image.load('pieces/black_queen.png')
  #KING
  #TODO

  def originalPieces(self):
    ret = {} 
    #PAWNS
    for col in self.columns:
      ret["%s2"%col] = self.white_pawn
    for col in self.columns:
      ret["%s7"%col] = self.black_pawn
    #ROOKS
    ret["A1"] = self.white_rook
    ret["H1"] = self.white_rook
    ret["A8"] = self.black_rook
    ret["H8"] = self.black_rook
    #KNIGHTS
    ret["B1"] = self.white_knight
    ret["G1"] = self.white_knight
    ret["B8"] = self.black_knight
    ret["G8"] = self.black_knight
    #BISHOPS
    ret["C1"] = self.white_bishop
    ret["F1"] = self.white_bishop
    ret["C8"] = self.black_bishop
    ret["F8"] = self.black_bishop
    #King
    #Queen
    ret["D1"] = self.white_queen
    ret["D8"] = self.black_queen

    return ret 

  def offsetImage(self, coords, img):
    if img == self.white_pawn or img == self.black_pawn:
      coords = (coords[0]+25, coords[1]+15)
    elif img == self.white_rook or img == self.black_rook:
      coords = (coords[0]+22, coords[1]+5)
    elif img == self.white_knight or img == self.black_knight:
      coords = (coords[0]+12, coords[1]+5)
    elif img == self.white_bishop or img == self.black_bishop:
      coords = (coords[0]+22, coords[1]+5)
    elif img == self.white_queen or img == self.black_queen:
      coords = (coords[0]+25, coords[1])

    return coords
  
  def legalSquares(self):
    moves = set() 
    for move in self.board.generate_legal_moves():
      if len(str(move))>4:
        continue
      moves.add(str(move)[:2])
    return moves
       
    

  def getRowsColumns(self):
    rows = self.rows
    columns = self.columns
    if not self.whiteAtBottom:
      rows = [z for z in reversed(self.rows)] 
      columns = [z for z in reversed(self.columns)]
    return rows, columns

  def getSquare(self, x, y):
    """ takes in coordinates, returns a {A-H}{0-8} string representing which square was pressed """
    rows, columns = self.getRowsColumns()

    column =  x//self.step
    row =     y//self.step
    return "%s%s"%(columns[column],rows[row])

  def getCoords(self, san):
    """ takes in SAN (A1, H8, etc) and returns the top left corner of the corresponding square"""
    rows, columns = self.getRowsColumns()
    column, row = san # subtly this splits the string `san` into A and 8, for example.
    row = int(row) # cast it to int
    column_index = columns.index(column)
    row_index = rows.index(row)
    return ( column_index*self.step,row_index*self.step)

  def generateMoves(self):
    moves = defaultdict(int)
    for move in self.board.generate_legal_moves():
      if len(str(move))>4:
        continue
      dest = str(move)[-2:].upper()
      moves[dest]+=1

    return moves 
      
  def generateOptions(self, square):
    moves = [] 
    for move in self.board.generate_legal_moves():
      if len(str(move))>4:
        continue
      if str(move)[:2].upper()==square:
        moves.append(str(move)[-2:].upper())

    return moves 
      
  def drawBlend(self, windowSurfaceObj, moves, threats):
    results = defaultdict(ColorTuple)
    for key, value in moves.items():
      results[key].b=min(100+(40*value),255)

    for key,value in threats.items():
      results[key].r=min(100+(40*value),255)

    for key, value in results.items():
      x, y = self.getCoords(key)
      pygame.draw.rect(windowSurfaceObj, pygame.Color(value.r, value.g, value.b), (x,y,self.step,self.step))
      
  def drawOptions(self, windowSurfaceObj, moves): 
    for square in moves:
      x,y = self.getCoords(square)
      color = pygame.Color(20,200,20) 
      pygame.draw.rect(windowSurfaceObj, color, (x,y,self.step,self.step))
      
      
  def drawCheckerboard(self, windowSurfaceObj):
    white = self.whiteColor
    black = self.blackColor
    for x in xrange(0,self.board_size,self.step):
      for y in xrange(0,self.board_size,self.step):
        switch = white if (x/self.step+y/self.step)%2==0 else black
        pygame.draw.rect(windowSurfaceObj, switch, (x,y,self.step,self.step))

  def drawPieces(self, windowSurfaceObj):
    for square, img in self.pieces.items():
      coords = self.getCoords(square)
      coords = self.offsetImage(coords, img)
      windowSurfaceObj.blit(img, coords) 
      

  def __init__(self):
    self.whiteAtBottom = True 
    self.board_size=801
    self.step=100
    self.pieces = self.originalPieces()

    self.board = chess.Bitboard()
    pygame.init()
    windowSurfaceObj = pygame.display.set_mode((self.board_size,self.board_size))
    pygame.display.set_caption("Chess Take 2, by Ben")

    clicks = []
    while True:
      self.drawCheckerboard(windowSurfaceObj)

      if len(clicks) == 0:
        moves = self.generateMoves() 
        self.board.push(None)
        threats = self.generateMoves()
        self.board.pop()
        self.drawBlend(windowSurfaceObj, moves, threats)
      if len(clicks) == 1:
        self.drawOptions(windowSurfaceObj, self.generateOptions(clicks[0]))

      self.drawPieces(windowSurfaceObj)


      for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
          assert self.getSquare(*event.pos) == self.getSquare(*self.getCoords(self.getSquare(*event.pos)))
          if len(clicks)==0:
            square = self.getSquare(*event.pos) 
            if square.lower() in self.legalSquares():
              clicks.append(square)
          else:
            origin = clicks[0]
            dest = self.getSquare(*event.pos)
            move = chess.Move( getattr(chess, clicks[0]), getattr(chess, dest))
            clicks = []
            if self.board.is_legal(move):
              self.pieces[dest] = self.pieces.pop(origin)
              self.board.push(move)
            
            
            

      pygame.display.update()

if __name__ == "__main__":
  HeatedChess()
