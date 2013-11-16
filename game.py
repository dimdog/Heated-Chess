import pygame, sys
import string
from pygame.locals import *
from piece import *
pygame.init()
board_size=801
windowSurfaceObj = pygame.display.set_mode((800,800))
pygame.display.set_caption("Chess, by Ben")
step=100
board = Board()
board.setup_board()
redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0,255,0)
blueColor = pygame.Color(0,0,255)

whiteColor = pygame.Color(255,255,255)
blackColor = pygame.Color(0,0,0)
#PIECES
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
def draw_loc_pawn(piece):
    return ((piece.location.x+1)*100-70,(piece.location.y+1)*100-80)
def draw_loc_knight(piece):
    return ((piece.location.x+1)*100-85,(piece.location.y+1)*100-95)
def draw_loc_bishop(piece):
    return ((piece.location.x+1)*100-80,(piece.location.y+1)*100-95)
def draw_loc_rook(piece):
    return ((piece.location.x+1)*100-80,(piece.location.y+1)*100-95)
def draw_loc_queen(piece):
    return ((piece.location.x+1)*100-80,(piece.location.y+1)*100-95)
def draw(piece):
    color = None 
    white = board.white
    black = board.black
    if piece.color==black:
        color = greenColor
    else:
        color = blueColor
    if isinstance(piece, Pawn):
        drawn_pawn = white_pawn if piece.color==white else black_pawn
        windowSurfaceObj.blit(drawn_pawn, draw_loc_pawn(piece))
    elif isinstance(piece, Knight):
        drawn_knight = white_knight if piece.color==white else black_knight
        windowSurfaceObj.blit(drawn_knight, draw_loc_knight(piece))
    elif isinstance(piece, Bishop):
        drawn_bishop = white_bishop if piece.color==white else black_bishop
        windowSurfaceObj.blit(drawn_bishop, draw_loc_bishop(piece))
    elif isinstance(piece, Rook):
        drawn_rook = white_rook if piece.color==white else black_rook
        windowSurfaceObj.blit(drawn_rook, draw_loc_rook(piece))
    elif isinstance(piece, Queen):
        drawn_queen = white_queen if piece.color==white else black_queen
        windowSurfaceObj.blit(drawn_queen, draw_loc_queen(piece))
    else:
        pygame.draw.rect(windowSurfaceObj, color, (((piece.location.x-1)*step)+step/4,((piece.location.y-1)*step)+step/4,step/2,step/2))

board.selected = None
greens = []
board.turn=board.white
def click_event(click_location):
  pass

def click_to_loc(click_location):
  mousex,mousey = click_location
  #normalize from pixels
  x = mousex/step
  y = mousey/step   
  # convert to chess format 
  x=string.ascii_uppercase[x]
  y=y+1
  
  print "%s%s"%(x,y)

  
while True:
    
  #draw checkerboard
  for x in xrange(0,board_size,step):
    for y in xrange(0,board_size,step):
      switch = whiteColor if (x/step+y/step)%2==0 else blackColor
      pygame.draw.rect(windowSurfaceObj, switch, (x,y,step,step))
  if greens:
    for square in greens:
      left = square[0]*step-step
      top = square[1]*step-step
      pygame.draw.rect(windowSurfaceObj, greenColor, (left,top,step,step))
  for piece in board.get_pieces():
    if not piece==None:
      draw(piece)

  for event in pygame.event.get():
    if event.type == MOUSEBUTTONUP:
      point = click_to_loc(event.pos)
#     ret_code, selected = board.click(click)
#     if selected:
#       greens = board.moves(selected.x,selected.y)
#       print greens
#     else:
#       greens = []
  pygame.display.update()
