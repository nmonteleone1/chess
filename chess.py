import pygame


####################--CONSTANTS--####################

#board size
sideSize = 480
squareSize = sideSize//8

#board colours
colour1 = (155,103,60)
colour2 = (230,206,168)
select1 = (234,76,70)
validMove = (255,255,102)


####################--GLOBALS--####################
squareColours = {}
currentSquare = 0

startSquare = {}
endSquare = {}

turn = 'w'

edgeDistance = {}
directionChanges = {}


####################--CLASSES--####################
class Piece:
	def __init__(self, type, image, team, moved):
		self.type = type
		self.image = image	
		self.team = team
		self.moved = moved


####################--FUNCTIONS--####################
def get_square():
	pos = pygame.mouse.get_pos()
	file = pos[0]//squareSize
	rank = pos[1]//squareSize
	return 8 * rank + file +1

def get_square_coordinates(square):
	x = ((square - 1) * squareSize)%sideSize
	y = (square - 1) // 8 * squareSize
	return (x,y)

def square_colour(square):
	loc = get_square_coordinates(square)
	return colour2 if (loc[0]/squareSize+loc[1]/squareSize)%2 == 0 else colour1

def draw_square(square):
	loc = get_square_coordinates(square)
	pygame.draw.rect(display_surface, squareColours[square], pygame.Rect(loc[0],loc[1],squareSize,squareSize))

def draw_board():
	for i in range(1,65):
		draw_square(i)

def draw_piece(i):
	if(startSquare.get(i,False)):
		loc = get_square_coordinates(i)
		piece = pygame.image.load(pieces.get(startSquare.get(i)).image)
		display_surface.blit(piece, (loc[0],loc[1]))

def draw_all_pieces():
	for i in range(1,65):
		draw_piece(i)

def refresh_board():
	draw_board()
	draw_all_pieces()

def deselect_square(square):
	squareColours[square] = square_colour(square)
	draw_square(square)

def select_square(square):
	loc = get_square_coordinates(square)
	square = get_square()

	global currentSquare
	if(square == currentSquare):
		deselect_square(square)
		currentSquare = 0
		return
	else:	
		deselect_square(currentSquare)
		currentSquare = square

	squareColours[square] = select1
	draw_square(square)
	draw_piece(square)

def drag_piece(piece):
	refresh_board()
	display_surface.blit(pygame.image.load(pieces.get(heldPiece).image), (pygame.mouse.get_pos()[0]-squareSize/2,pygame.mouse.get_pos()[1]-squareSize/2))

def move_piece(startPos, endPos):
	if startPos == endPos:
		return

	for i in endSquare.get(startPos):
		if i == endPos:
			startSquare[heldPiece].moved = True
			startSquare.pop(startPos)
			startSquare[endPos] = heldPiece

			for j in endSquare.get(startPos):
				deselect_square(j)

def valid_sliding_moves(square):
	movePiece = pieces.get(startSquare.get(square))
	endSquare[square] = []

	startIndex = 4 if movePiece.type == 'bishop' else 0
	endIndex = 4 if movePiece.type == 'rook' else 8
	for i in range(startIndex,endIndex):
		for j in range(1,edgeDistance.get(square)[i]+1):
			print(j)
			attackSquare = square + directionChanges[i]*j
			print(attackSquare)
			attackPiece = pieces.get(startSquare.get(attackSquare))

			if attackPiece != None and movePiece.team == attackPiece.team:
				break

			endSquare[square].append(attackSquare)
			squareColours[attackSquare] = validMove

			if attackPiece != None:
				break

def valid_pawn_moves(square):
	movePiece = pieces.get(startSquare.get(square))
	endSquare[square] = []

	if movePiece.team == 'w':
		if movePiece.moved == False:
			endSquare[square].append(square-16)

		attack1 = square-9
		attack2 = square-7

		if edgeDistance.get(square)[0] > 0:
			if pieces.get(startSquare.get(attack1)) and edgeDistance.get(square)[2] > 0:
				endSquare[square].append(attack1)
			if pieces.get(startSquare.get(attack2)) and edgeDistance.get(square)[3] > 0:
				endSquare[square].append(attack2)

			endSquare[square].append(square-8)
	elif movePiece.team == 'b':
		if movePiece.moved == False:
			endSquare[square].append(square+16)

		attack1 = square+7
		attack2 = square+9

		if edgeDistance.get(square)[1] > 0:
			if pieces.get(startSquare.get(attack1)) and edgeDistance.get(square)[2] > 0:
				endSquare[square].append(attack1)
			if pieces.get(startSquare.get(attack2)) and edgeDistance.get(square)[3] > 0:
				endSquare[square].append(attack2)

			endSquare[square].append(square+8)

def find_valid_moves(square):
	switch
	startSquare[square].type


####################--INIT--####################
pygame.init()
pygame.display.set_caption('Chess')
display_surface = pygame.display.set_mode((sideSize, sideSize))
done = False
hold = False
heldPiece = None
heldPieceStart = None
heldPieceEnd = None

#generate chess board
for i in range(1,65):
	squareColours[i] = square_colour(i)
draw_board()

#calculate distance to edges for each square
for i in range(0,8):
	for j in range(0,8):
		up = j
		down = 7-j
		left = i
		right = 7-i
		upleft = min(up,left)
		upright = min(up,right)
		downleft = min(down,left)
		downright = min(down,right)

		square = i + j * 8 + 1

		edgeDistance[square] = [up,down,left,right,upleft,upright,downleft,downright]
directionChanges = [-8,8,-1,1,-9,-7,7,9]

#dict for piece lookup
pieces = {
	'r' : Piece('rook', 'b_rook.png', 'b', False),
	'n' : Piece('knight', 'b_knight.png', 'b', False),
	'b' : Piece('bishop', 'b_bishop.png', 'b', False),
	'q' : Piece('queen', 'b_queen.png', 'b', False),
	'k' : Piece('king', 'b_king.png', 'b', False),
	'p' : Piece('pawn', 'b_pawn.png', 'b', False),
	'R' : Piece('rook', 'w_rook.png', 'w', False),
	'N' : Piece('knight', 'w_knight.png', 'w', False),
	'B' : Piece('bishop', 'w_bishop.png', 'w', False),
	'Q' : Piece('queen', 'w_queen.png', 'w', False),
	'K' : Piece('king', 'w_king.png', 'w', False),
	'P' : Piece('pawn', 'w_pawn.png', 'w', False)
}

#populate board
FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

squareCounter = 1
for char in FEN:
	if char.isnumeric():
		squareCounter += int(char)
		continue
	elif char == '/':
		continue
	else:
		startSquare[squareCounter] = char
		squareCounter += 1
		continue

#draw pieces
draw_all_pieces()


####################--RUN LOOP--####################
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

		elif event.type == pygame.MOUSEBUTTONDOWN:
			hold = True
			heldPieceStart = get_square()
			heldPiece = startSquare.get(heldPieceStart)
			if(heldPiece):
				select_square(heldPieceStart)
				valid_sliding_moves(heldPieceStart)
				print(edgeDistance.get(heldPieceStart))
				print(endSquare.get(heldPieceStart))
			refresh_board()

		elif event.type == pygame.MOUSEBUTTONUP:
			if(heldPiece != None and heldPieceStart != None):
				heldPieceEnd = get_square()
				move_piece(heldPieceStart, heldPieceEnd)

				heldPieceStart = None
				heldPieceEnd = None			
			
			hold = False
			refresh_board()

		elif event.type == pygame.MOUSEMOTION:
			if hold == True and heldPiece != None:
				drag_piece(heldPiece)
			
		

		
	pygame.display.flip()

