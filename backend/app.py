import chess
from flask import Flask
from collections import defaultdict
import simplejson as json

app = Flask(__name__)


class HeatedChess:
    columns = ["A", "B", "C", "D", "E", "F", "G", "H"]
    rows = [8, 7, 6, 5, 4, 3, 2, 1]

    def __init__(self):
        self.board = chess.Board()

    def generateData(self):
        """ generates data:
            - Piece locations: {"E2" : {"type" = "pawn", "location" : "E2", "color" : "white"}}
            - White threats: ["E3","B3","C3"]...
            - Black threats: ["E3","B3","C3"]...
            - Moves: {"E2" : ["A3", "F5"]}
            - Player turn: "white"
            """
        pieces = {}
        white_threats = defaultdict(list)
        black_threats = defaultdict(list)
        for row in self.rows:
            for column in self.columns:
                square_name = "{}{}".format(column, row)
                target_square = getattr(chess, square_name)
                chess_piece = self.board.piece_at(target_square)
                if chess_piece:
                    piece = {
                            'location': square_name,
                            'color': chess.COLOR_NAMES[chess_piece.color],
                            'type': chess.PIECE_NAMES[chess_piece.piece_type]
                            }
                    pieces[piece['location']] = piece
                for dest_square_int in self.board.attackers(chess.WHITE, target_square):
                    white_threats[square_name].append(chess.SQUARE_NAMES[dest_square_int].upper())
                for dest_square_int in self.board.attackers(chess.BLACK, target_square):
                    black_threats[square_name].append(chess.SQUARE_NAMES[dest_square_int].upper())
        return {
                    "pieces": pieces,
                    "white_threats": white_threats,
                    "black_threats": black_threats,
                    "moves": self.generateMoves(),
                    "turn": chess.COLOR_NAMES[self.board.turn]
               }

    def generateMoves(self):
        moves = defaultdict(list)
        for move in self.board.generate_legal_moves():
            move_str = str(move).upper()
            source = move_str[:2]
            dest = move_str[2:]
            moves[source].append(dest)

        return moves


#  def draw(self):
#      threats, supports = self.generateThreatsSupports()
#      for event in pygame.event.get():
#        if event.type == MOUSEBUTTONUP:
#          assert self.getSquare(*event.pos) == self.getSquare(*self.getCoords(self.getSquare(*event.pos)))
#          if len(clicks)==0:
#            square = self.getSquare(*event.pos)
#            if square.lower() in self.legalSquares():
#              clicks.append(square)
#          else:
#            origin = clicks[0]
#            dest = self.getSquare(*event.pos)
#            move = chess.Move( getattr(chess, clicks[0]), getattr(chess, dest))
#            clicks = []
#            if self.board.is_legal(move):
#              self.pieces[dest] = self.pieces.pop(origin)
#              self.board.push(move)

hc = HeatedChess()

@app.route("/api")
def hello():
    return json.dumps(hc.generateData())

if __name__ == "__main__":
    app.run()
