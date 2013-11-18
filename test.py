from piece import *
from board import *
import unittest

class TestChess(unittest.TestCase):
  
  def setUp(self):
    self.board = Board()
  
  
  def test_setup_board(self):
    def piece_and_color(pos, piece, color):
      self.assertEqual(isinstance(self.board.get_piece(pos), piece),True)
      self.assertEqual(self.board.get_piece(pos).color, color)
      
    self.board.setup_board()
    print self.board
    white = self.board.white
    black = self.board.black
    #pawns!
    for column in ['a%s','b%s','c%s','d%s','e%s','f%s','g%s','h%s']:
      self.assertEqual(isinstance(self.board.get_piece(column%2), Pawn), True)
      self.assertEqual(self.board.get_piece(column%2).color, white)
      print "Pass: %s"%column%2

      self.assertEqual(isinstance(self.board.get_piece(column%7), Pawn), True)
      self.assertEqual(self.board.get_piece(column%7).color, black)
    #rooks!
    piece_and_color("A1", Rook, white)
    piece_and_color("H1", Rook, white)
    piece_and_color("A8", Rook, black)
    piece_and_color("H8", Rook, black)
    #knights!
    piece_and_color("B1", Knight, white)
    piece_and_color("G1", Knight, white)
    piece_and_color("B8", Knight, black)
    piece_and_color("G8", Knight, black)
    #bishops!
    piece_and_color("C1", Bishop, white)
    piece_and_color("F1", Bishop, white)
    piece_and_color("C8", Bishop, black)
    piece_and_color("F8", Bishop, black)
    #King!
    piece_and_color("E1", King, white)
    piece_and_color("E8", King, black)
    #Queen
    piece_and_color("D1", Queen, white)
    piece_and_color("D8", Queen, black)
     
  def test_pawn(self):
    self.board.setup_board()
    print self.board.moves()
    
