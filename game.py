import pygame, sys, chess
from pygame.locals import *

class HeatedChess:
  columns = ["A","B","C","D","E","F","G","H"] 
  rows = [8,7,6,5,4,3,2,1]
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
    
  def drawCheckerboard(self, windowSurfaceObj):
    white = self.whiteColor
    black = self.blackColor
    for x in xrange(0,self.board_size,self.step):
      for y in xrange(0,self.board_size,self.step):
        switch = white if (x/self.step+y/self.step)%2==0 else black
        pygame.draw.rect(windowSurfaceObj, switch, (x,y,self.step,self.step))

  def __init__(self):
    self.whiteAtBottom = True 
    self.board_size=801
    self.step=100
    self.whiteColor = pygame.Color(255,255,255)
    self.blackColor = pygame.Color(0,0,0)

    board = chess.Bitboard()
    pygame.init()
    windowSurfaceObj = pygame.display.set_mode((self.board_size,self.board_size))
    pygame.display.set_caption("Chess Take 2, by Ben")
    while True:
      self.drawCheckerboard(windowSurfaceObj)
      for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
          assert self.getSquare(*event.pos) == self.getSquare(*self.getCoords(self.getSquare(*event.pos)))

      pygame.display.update()

if __name__ == "__main__":
  HeatedChess()
