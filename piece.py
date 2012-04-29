from collections import namedtuple
white=0
black=1
whitelist=None
blacklist=None
global board
board=[[]]
turn=None
whiteking=None
blackking=None
in_passing=False
last_move=None
Point = namedtuple('Point','x y')
Move = namedtuple('Move','origin destination piece')
class Piece:
    def __init__(self,x,y,color):
        self.location=Point(x,y)
        self.color=color
    
    def square(self,destination):
        return ((1 <= destination.x <= 8) and (1 <= destination.y <= 8))
    
    def rook_move(self,destination): #this is here as a convienence so queen can call this code too
        if self.location.x-destination.x!=0 and self.location.y-destination.y==0:
            for i in range(min(self.location.x,destination.x),max(self.location.x,destination.x)):
                print i
                if occupied(Point(i,self.location.y)):
                    return False
            return not occupied(destination,self.color)
        if self.location.y-destination.y!=0 and self.location.x-destination.x==0:
            for i in range(min(self.location.y,destination.y),max(self.location.y,destination.y)):
                print i
                if occupied(Point(self.location.x,i)):
                    return False
            return not occupied(destination,self.color)
        return False


    def bishop_move(self,destination): #this is here as a convienence so queen can call this code too
        if abs(self.location.x-destination.x)==abs(self.location.y-destination.y):
            for x,y in zip(range(min(self.location.x,destination.x),max(self.location.x,destination.x)),range(min(self.location.y,destination.y),max(self.location.y,destination.y))):
                if occupied(Point(x,y)):
                    return False
            return not occupied(destination,self.color)
        return False
    
    def __str__(self):
        c = "White" if self.color==white else "Black"
        return  "%s %s"%(c, self.__class__)
class Pawn(Piece):
    
    def move(self,destination):
        if not self.square(destination):
            return False
        switch = -1
        if self.color==black:
            switch=1

        if self.location.y+switch==destination.y and abs(self.location.x-destination.x)==1: # attacking
            return occupied(destination,self.color) or self.en_passent(destination,switch)
        elif  self.location.x-destination.x==0: # advancing
            if self.location.y+switch==destination.y:
                return not occupied(destination)
            elif self.location.y+(switch*2)==destination.y and ((self.color==white and self.location.y==7) or (self.color==black and self.location.y==2)): # Double advancing
                close_destination = Point(destination.x,destination.y-switch)
                return not (occupied(destination) and occupied(close_destination))
        
    def en_passent(self,destination,switch):
        last_move=previous_move()
        in_passing = False
        if last_move:
            in_passing = isinstance(last_move.piece, Pawn) and destination.y-switch==last_move.destination.y and destination.x==last_move.x and destination.y+switch==last_move.origin
        return in_passing
            

class King(Piece):
    
    def move(self,destination):
        return self.square(destination) and self.close(destination) and not occupied(destination,self.color) and safe(destination,self.color)
    
    def close(self,destination):
        return abs(self.location.x-destination.x)==1 and abs(self.location.y-destination.y)==1

class Knight(Piece):

    def move(self,destination):
        #this one just has a ton of checks for the multitude of combinations possible
        return self.square(destination) and (not occupied(destination,self.color)) and ((abs(self.location.x-destination.x)==2 and abs(self.location.y-destination.y)==1) or  (abs(self.location.x-destination.x)==1 and abs(self.location.y-destination.y)==2)) # need it to check for the other color

class Bishop(Piece):
    
    def move(self,destination):
        return self.square(destination) and self.bishop_move(destination)

class Queen(Piece):

    def move(self,destination):
        return self.square(destination) and (self.bishop_move(destination) or self.rook_move(destination))

class Rook(Piece):

    def move(self,destination):
        return self.square(destination) and self.rook_move(destination)


###################


def setup_board():
    selected=None
    turn=white
    blacklist=[Rook(1,1,black),Rook(8,1,black),Knight(2,1,black),Knight(7,1,black),Bishop(3,1,black),Bishop(6,1,black),Queen(4,1,black),King(5,1,black)]#+ pawns
    whitelist=[Rook(1,8,white),Rook(8,8,white),Knight(2,8,white),Knight(7,8,white),Bishop(3,8,white),Bishop(6,8,white),Queen(4,8,white),King(5,8,white)]#+ pawns
    for i in range(1,9):
        blacklist.append(Pawn(i,2,black))
        whitelist.append(Pawn(i,7,white))
    w, h = 9,9
    combined = whitelist
    combined.extend(blacklist)
    global board
    board = [[None] * w for i in range(h)]
    for piece in combined:    
        board[piece.location.x][piece.location.y]=piece
    return board



def click(clicked, selected): # Click event!
    if occupied(clicked):
        if selected==None and occupied(clicked,turn):
            selected=clicked
            return True, selected
    if not selected==None:
        piece = get_piece(selected)
        print "move? %s"%piece.move(clicked)
        if piece.move(clicked) and safe(king(turn)):
            print "got here"
            global board
            if in_passing:
                switch = 1
                if self.color==white:
                    switch=-1
                board[clicked.x][clicked.y-switch]=None

            board[clicked.x][clicked.y]=piece
            piece.location=clicked
            last_move=Move(selected,clicked,piece)
            selected = None
            return True, selected
    selected = None
    return False, selected


#################

def moves(locx,locy):
    global board
    print "click:",locx, locy
    ret = []
    for x in range(8):
        for y in range(8):
            if board[locx][locy].move(Point(x+1,y+1)):
                print "yes"
                ret.append((x+1,y+1))
    return ret

def other_turn():
    if turn==white:
        return black
    return white


def safe(destination, color): # checks to see if a destination is under threat from a piece of the opposite color
    for piece in get_pieces(color):
        if not isinstance(piece, King):
            if piece.move(destination):
                return False
    return True

def get_pieces(color=None): #returns a list of all the pieces with no arguments, and all pieces of the opposite color if given a color)
    global board
    whitelist = blacklist = combined = []
    for row in board:
        for piece in row:
            if isinstance(piece, Piece):
                if color==None:
                    combined.append(piece)
                else:
                    if piece.color == black:
                        blacklist.append(piece)
                    else:
                        whitelist.append(piece)

    if color==None:
        return combined
    if color==black:
        return whitelist
    else:
        return blacklist

def occupied(destination, color=None): # checks to see if destination is occupied and a piece of the opposite color, if nothing is provided, will check for any color
    piece=get_piece(destination)
    if piece:
        return piece.color==color
    else:
        return False

def previous_move(): #returns a move object containing a piece, destination, and origin.       
    return last_move

def king(turn): # this will have its logic replaced with a lookup to a global when we start loading in boards turn by turn, for now, for loop!
    global board
    for row in board:
        for piece in row:
            if isinstance(piece, King) and piece.color==turn:
                return piece
    return None
 
def get_piece(destination):
    global board
    try:
        return board[destination.x][destination.y]
    except IndexError:
        return None

