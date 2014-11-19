import pygame, sys
from pygame.locals import *

class HeatedChess:
  board_size=801
  step=100
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

  def drawCheckerboard(self, windowSurfaceObj):
    for x in xrange(0,self.board_size,self.step):
      for y in xrange(0,self.board_size,self.step):
        switch = self.whiteColor if (x/self.step+y/self.step)%2==0 else self.blackColor
        pygame.draw.rect(windowSurfaceObj, switch, (x,y,self.step,self.step))

  def __init__(self):
    pygame.init()
    windowSurfaceObj = pygame.display.set_mode((self.board_size,self.board_size))
    pygame.display.set_caption("Chess Take 2, by Ben")
    while True:
      self.drawCheckerboard(windowSurfaceObj)
      pygame.display.update()

if __name__ == "__main__":
  HeatedChess()
