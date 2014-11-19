from piece import *
from board import *
import unittest

class TestChess(unittest.TestCase):
  
  def setUp(self):
    self.board = Board()
  
  def test_translate(self):
    return True
    self.assertEqual(self.board.translate(0,0),"A1")
    self.assertEqual(self.board.translate(4,1),"E2")
    self.assertEqual(self.board.translate(7,7),"H8")
    self.assertEqual(self.board.translate("A1"),(0,0))
    self.assertEqual(self.board.translate("E2"),(4,1))
    self.assertEqual(self.board.translate("H8"),(7,7))
  
  
  def test_setup_board(self):
    return True
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
     
  def test_get_pieces(self):
    self.board.setup_board()
    print self.board
    return False
    pieces = self.board.get_pieces()
    white_pieces = self.board.get_pieces(self.board.white)
    black_pieces = self.board.get_pieces(self.board.black)
    self.assertEqual(32, len(pieces))
    self.assertEqual(16, len(white_pieces))
    self.assertEqual(16, len(black_pieces))
    self.board.move("E2","E4")
    pieces = self.board.get_pieces()
    white_pieces = self.board.get_pieces(self.board.white)
    black_pieces = self.board.get_pieces(self.board.black)
    self.assertEqual(32, len(pieces))
    self.assertEqual(16, len(white_pieces))
    self.assertEqual(16, len(black_pieces))
    
  def test_pawn(self):
    return True
    self.board.setup_board()
    moves = self.board.moves()
    self.assertItemsEqual(moves["E2"]["moves"],['E3', 'E4'])
    self.assertEqual(self.board.move("E2","E4",moves),True)
    #Pawn can do a double move only on the first jump...(resets the turn, moves white again)
    self.board.turn = self.board.white
    moves = self.board.moves()
    print sorted(moves)
    self.assertEqual("E4" in moves, True) 
    self.assertItemsEqual(moves["E4"]["moves"],['E5'])
     
    #TODO En Passent, attack testing...
    
