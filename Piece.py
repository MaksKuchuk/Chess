import pygame as pg

def beaten(board, color):
	b = [[0 for i in range(8)] for j in range(8)]

	for i in range(8):
		for j in range(8):
			if board[i][j]:
				if board[i][j].color != color:
					for p in board[i][j].killWays((i, j), board):
						b[p[0]][p[1]] = 1

	return b

def safeFromCheck(board, to_pos, figure):
	is_safe = True
	t = board[to_pos[0]][to_pos[1]]
	board[to_pos[0]][to_pos[1]] = figure

	if isCheck(board, figure.color):
		is_safe = False

	board[to_pos[0]][to_pos[1]] = t

	return is_safe

def isCheck(board, color):
	a = beaten(board, color)

	for i in range(8):
		for j in range(8):
			if board[i][j]:
				if board[i][j].color == color and board[i][j].ty() == "King" and a[i][j]:
					return True
	return False
	

class Pawn:
	def __init__(self, color, cell_scale):
		self.is_ghost = True
		self.is_first = True
		self.color = color
		self.img = pg.transform.scale(pg.image.load("img/bP.png" if self.color == 'b' else "img/wP.png"), (cell_scale[0], cell_scale[1]))

	def isStep(self, pos, board):
		a = []
		if self.color == 'w':
			if self.is_first and board[pos[0]][pos[1] - 1] == 0:
				if board[pos[0]][pos[1] - 2] == 0:
					if safeFromCheck(board, (pos[0], pos[1] - 2), self):
						a.append((pos[0], pos[1] - 2))

			if board[pos[0]][pos[1] - 1] == 0:
				if safeFromCheck(board, (pos[0], pos[1] - 1), self):
					a.append((pos[0], pos[1] - 1))

		else:
			if self.is_first and board[pos[0]][pos[1] + 1] == 0:
				if board[pos[0]][pos[1] + 2] == 0:
					if safeFromCheck(board, (pos[0], pos[1] + 2), self):
						a.append((pos[0], pos[1] + 2))

			if board[pos[0]][pos[1] + 1] == 0:
				if safeFromCheck(board, (pos[0], pos[1] + 1), self):
					a.append((pos[0], pos[1] + 1))
		return a

	def isKill(self, pos, board):
		a = []

		if self.color == 'w': 
			steps = ((-1, -1), (1, -1))
			for i in steps:
				if 0 <= pos[0] + i[0] < 8 and 0 <= pos[1] + i[1] < 8:
					if board[pos[0] + i[0]][pos[1] + i[1]] != 0:
						if board[pos[0] + i[0]][pos[1] + i[1]].color != self.color:
							if safeFromCheck(board, (pos[0] + i[0], pos[1] + i[1]), self):
								a.append((pos[0] + i[0], pos[1] + i[1]))
					else:
						if board[pos[0] + i[0]][pos[1]]:
							if board[pos[0] + i[0]][pos[1]].ty() == "Pawn":
								if board[pos[0] + i[0]][pos[1]].color != self.color and board[pos[0] + i[0]][pos[1]].is_ghost:
									if safeFromCheck(board, (pos[0] + i[0], pos[1]), self):
										a.append((pos[0] + i[0], pos[1] + i[1]))
		else:
			steps = ((1, 1), (-1, 1))
			for i in steps:
				if 0 <= pos[0] + i[0] < 8 and 0 <= pos[1] + i[1] < 8:
					if board[pos[0] + i[0]][pos[1] + i[1]] != 0:
						if board[pos[0] + i[0]][pos[1] + i[1]].color != self.color:
							if safeFromCheck(board, (pos[0] + i[0], pos[1] + i[1]), self):
								a.append((pos[0] + i[0], pos[1] + i[1]))
					else:
						if board[pos[0] + i[0]][pos[1]]:
							if board[pos[0] + i[0]][pos[1]].ty() == "Pawn":
								if board[pos[0] + i[0]][pos[1]].color != self.color and board[pos[0] + i[0]][pos[1]].is_ghost:
									if safeFromCheck(board, (pos[0] + i[0], pos[1]), self):
										a.append((pos[0] + i[0], pos[1] + i[1]))
		return a

	def killWays(self, pos, board):
		a = []

		if self.color == 'w': 
			steps = ((-1, -1), (1, -1))
			for i in steps:
				if 0 <= pos[0] + i[0] < 8 and 0 <= pos[1] + i[1] < 8:
					if board[pos[0] + i[0]][pos[1] + i[1]] != 0:
						if board[pos[0] + i[0]][pos[1] + i[1]].color != self.color:
							a.append((pos[0] + i[0], pos[1] + i[1]))
					else:
						a.append((pos[0] + i[0], pos[1] + i[1]))
		else:
			steps = ((1, 1), (-1, 1))
			for i in steps:
				if 0 <= pos[0] + i[0] < 8 and 0 <= pos[1] + i[1] < 8:
					if board[pos[0] + i[0]][pos[1] + i[1]] != 0:
						if board[pos[0] + i[0]][pos[1] + i[1]].color != self.color:
							a.append((pos[0] + i[0], pos[1] + i[1]))
					else:
						a.append((pos[0] + i[0], pos[1] + i[1]))

		return a

	def ty(self):
		return "Pawn"


class Rock:
	def __init__(self, color, cell_scale):
		self.is_first = True
		self.color = color
		self.img = pg.transform.scale(pg.image.load("img/bR.png" if self.color == 'b' else "img/wR.png"), (cell_scale[0], cell_scale[1]))

	def isStep(self, pos, board):
		a = []

		for i in range(pos[0] + 1, 8):
			if board[i][pos[1]] == 0:
				if safeFromCheck(board, (i, pos[1]), self):
					a.append((i, pos[1]))
			else: 
				break

		for i in range(pos[0] - 1, -1, -1):
			if board[i][pos[1]] == 0:
				if safeFromCheck(board, (i, pos[1]), self):
					a.append((i, pos[1]))
			else: 
				break

		for i in range(pos[1] + 1, 8):
			if board[pos[0]][i] == 0:
				if safeFromCheck(board, (i, pos[1]), self):
					a.append((pos[0], i))
			else: 
				break

		for i in range(pos[1] - 1, -1, -1):
			if board[pos[0]][i] == 0:
				if safeFromCheck(board, (i, pos[1]), self):
					a.append((pos[0], i))
			else: 
				break
		return a

	def isKill(self, pos, board):
		a = []

		for i in range(pos[0] + 1, 8):
			if board[i][pos[1]]:
				if board[i][pos[1]].color != self.color:
					if safeFromCheck(board, (i, pos[1]), self):
						a.append((i, pos[1]))
				break

		for i in range(pos[0] - 1, -1, -1):
			if board[i][pos[1]]:
				if board[i][pos[1]].color != self.color:
					if safeFromCheck(board, (i, pos[1]), self):
						a.append((i, pos[1]))
				break

		for i in range(pos[1] + 1, 8):
			if board[pos[0]][i]:
				if board[pos[0]][i].color != self.color:
					if safeFromCheck(board, (pos[0], i), self):
						a.append((pos[0], i))
				break

		for i in range(pos[1] - 1, -1, -1):
			if board[pos[0]][i]:
				if board[pos[0]][i].color != self.color:
					if safeFromCheck(board, (pos[0], i), self):
						a.append((pos[0], i))
				break
		return a

	def killWays(self, pos, board):
		a = []

		for i in range(pos[0] + 1, 8):
			if board[i][pos[1]] == 0:
				a.append((i, pos[1]))
			else: 
				if board[i][pos[1]].color != self.color:
					a.append((i, pos[1]))
				break

		for i in range(pos[0] - 1, -1, -1):
			if board[i][pos[1]] == 0:
				a.append((i, pos[1]))
			else: 
				if board[i][pos[1]].color != self.color:
					a.append((i, pos[1]))
				break

		for i in range(pos[1] + 1, 8):
			if board[pos[0]][i] == 0:
				a.append((pos[0], i))
			else: 
				if board[pos[0]][i].color != self.color:
					a.append((pos[0], i))
				break

		for i in range(pos[1] - 1, -1, -1):
			if board[pos[0]][i] == 0:
				a.append((pos[0], i))
			else: 
				if board[pos[0]][i].color != self.color:
					a.append((pos[0], i))
				break

		return a

	def ty(self):
		return "Rock"


class Knight:
	def __init__(self, color, cell_scale):
		self.is_first = True
		self.color = color
		self.img = pg.transform.scale(pg.image.load("img/bN.png" if self.color == 'b' else "img/wN.png"), (cell_scale[0], cell_scale[1]))

	def isStep(self, pos, board):
		steps = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
		a = []

		for i in steps:
			if 0 <= pos[0] + i[0] < 8 and 0 <= pos[1] + i[1] < 8:
				if board[pos[0] + i[0]][pos[1] + i[1]] == 0:
					if safeFromCheck(board, (pos[0] + i[0], pos[1] + i[1]), self):
						a.append((pos[0] + i[0], pos[1] + i[1]))
		return a

	def isKill(self, pos, board):
		steps = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
		a = []

		for i in steps:
			if 0 <= pos[0] + i[0] < 8 and 0 <= pos[1] + i[1] < 8:
				if board[pos[0] + i[0]][pos[1] + i[1]]:
					if board[pos[0] + i[0]][pos[1] + i[1]].color != self.color:
						if safeFromCheck(board, (pos[0] + i[0], pos[1] + i[1]), self):
							a.append((pos[0] + i[0], pos[1] + i[1]))
		return a

	def killWays(self, pos, board):
		steps = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
		a = []

		for i in steps:
			if 0 <= pos[0] + i[0] < 8 and 0 <= pos[1] + i[1] < 8:
				if board[pos[0] + i[0]][pos[1] + i[1]] == 0:
					a.append((pos[0] + i[0], pos[1] + i[1]))
				else:
					if board[pos[0] + i[0]][pos[1] + i[1]].color != self.color:
						a.append((pos[0] + i[0], pos[1] + i[1]))
		return a

	def ty(self):
		return "Knight"


class Bishop:
	def __init__(self, color, cell_scale):
		self.is_first = True
		self.color = color
		self.img = pg.transform.scale(pg.image.load("img/bB.png" if self.color == 'b' else "img/wB.png"), (cell_scale[0], cell_scale[1]))

	def isStep(self, pos, board):
		a = []

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] + i][pos[1] + i] == 0:
					if safeFromCheck(board, (pos[0] + i, pos[1] + i), self):
						a.append((pos[0] + i, pos[1] + i))
				else: break
			else: break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] - i][pos[1] - i] == 0:
					if safeFromCheck(board, (pos[0] - i, pos[1] - i), self):
						a.append((pos[0] - i, pos[1] - i))
				else: break
			else: break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] - i][pos[1] + i] == 0:
					if safeFromCheck(board, (pos[0] - i, pos[1] + i), self):
						a.append((pos[0] - i, pos[1] + i))
				else: break
			else: break

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] + i][pos[1] - i] == 0:
					if safeFromCheck(board, (pos[0] + i, pos[1] - i), self):
						a.append((pos[0] + i, pos[1] - i))
				else: break
			else: break
		return a

	def isKill(self, pos, board):
		a = []

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] + i][pos[1] + i]:
					if board[pos[0] + i][pos[1] + i].color != self.color:
						if safeFromCheck(board, (pos[0] + i, pos[1] + i), self):
							a.append((pos[0] + i, pos[1] + i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] - i][pos[1] - i]:
					if board[pos[0] - i][pos[1] - i].color != self.color:
						if safeFromCheck(board, (pos[0] - i, pos[1] - i), self):
							a.append((pos[0] - i, pos[1] - i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] - i][pos[1] + i]:
					if board[pos[0] - i][pos[1] + i].color != self.color:
						if safeFromCheck(board, (pos[0] - i, pos[1] + i), self):
							a.append((pos[0] - i, pos[1] + i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] + i][pos[1] - i]:
					if board[pos[0] + i][pos[1] - i].color != self.color:
						if safeFromCheck(board, (pos[0] + i, pos[1] - i), self):
							a.append((pos[0] + i, pos[1] - i))
					break
		return a

	def killWays(self, pos, board):
		a = []

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] + i][pos[1] + i] == 0:
					a.append((pos[0] + i, pos[1] + i))
				else: 
					if board[pos[0] + i][pos[1] + i].color != self.color:
						a.append((pos[0] + i, pos[1] + i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] - i][pos[1] - i] == 0:
					a.append((pos[0] - i, pos[1] - i))
				else:
					if board[pos[0] - i][pos[1] - i].color != self.color:
						a.append((pos[0] - i, pos[1] - i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] - i][pos[1] + i] == 0:
					a.append((pos[0] - i, pos[1] + i))
				else:
					if board[pos[0] - i][pos[1] + i].color != self.color:
						a.append((pos[0] - i, pos[1] + i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] + i][pos[1] - i] == 0:
					a.append((pos[0] + i, pos[1] - i))
				else:
					if board[pos[0] + i][pos[1] - i].color != self.color:
						a.append((pos[0] + i, pos[1] - i))
					break

		return a

	def ty(self):
		return "Bishop"


class King:
	def __init__(self, color, cell_scale):
		self.is_first = True
		self.color = color
		self.img = pg.transform.scale(pg.image.load("img/bK.png" if self.color == 'b' else "img/wK.png"), (cell_scale[0], cell_scale[1]))

	def isStep(self, pos, board):
		steps = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
		a = []

		for i in steps:
			if 0 <= pos[0] + i[0] < 8 and 0 <= pos[1] + i[1] < 8:
				if board[pos[0] + i[0]][pos[1] + i[1]] == 0:
					if safeFromCheck(board, (pos[0] + i[0], pos[1] + i[1]), self):
						a.append((pos[0] + i[0], pos[1] + i[1]))
		return a

	def isKill(self, pos, board):
		steps = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
		a = []

		for i in steps:
			if 0 <= pos[0] + i[0] < 8 and 0 <= pos[1] + i[1] < 8:
				if board[pos[0] + i[0]][pos[1] + i[1]]:
					if board[pos[0] + i[0]][pos[1] + i[1]].color != self.color:
						if safeFromCheck(board, (pos[0] + i[0], pos[1] + i[1]), self):
							a.append((pos[0] + i[0], pos[1] + i[1]))

		return a

	def killWays(self, pos, board):
		steps = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
		a = []

		for i in steps:
			if 0 <= pos[0] + i[0] < 8 and 0 <= pos[1] + i[1] < 8:
				if board[pos[0] + i[0]][pos[1] + i[1]] == 0:
					a.append((pos[0] + i[0], pos[1] + i[1]))
				else:
					if board[pos[0] + i[0]][pos[1] + i[1]].color != self.color:
						a.append((pos[0] + i[0], pos[1] + i[1]))
		return a

	def ty(self):
		return "King"

	def isCastling(self, pos, board):
		a = beaten(board, self.color)

		p = [False, False]

		if a[4][7]:
			return p

		if self.color == 'w' and self.is_first and board[7][7]:
			if board[7][7].is_first and not board[5][7] and not board[6][7] and not a[5][7] and not a[6][7]:
				p[1] = True
		
		if self.color == 'w' and self.is_first and board[0][7]:
			if board[0][7].is_first and not board[1][7] and not board[2][7] and not board[3][7] and not a[1][7] and not a[2][7] and not a[3][7]:
				p[0] = True

		if self.color == 'b' and self.is_first and board[7][0]:
			if board[7][0].is_first and not board[5][0] and not board[6][0] and not a[5][0] and not a[6][0]:
				p[1] = True
		
		if self.color == 'b' and self.is_first and board[0][0]:
			if board[0][0].is_first and not board[1][0] and not board[2][0] and not board[3][0] and not a[1][0] and not a[2][0] and not a[3][0]:
				p[0] = True

		return p

class Queen:
	def __init__(self, color, cell_scale):
		self.is_first = True
		self.color = color
		self.img = pg.transform.scale(pg.image.load("img/bQ.png" if self.color == 'b' else "img/wQ.png"), (cell_scale[0], cell_scale[1]))

	def isStep(self, pos, board):
		a = []

		for i in range(pos[0] + 1, 8):
			if board[i][pos[1]] == 0:
				if safeFromCheck(board, (i, pos[1]), self):
					a.append((i, pos[1]))
			else: 
				break

		for i in range(pos[0] - 1, -1, -1):
			if board[i][pos[1]] == 0:
				if safeFromCheck(board, (i, pos[1]), self):
					a.append((i, pos[1]))
			else: 
				break

		for i in range(pos[1] + 1, 8):
			if board[pos[0]][i] == 0:
				if safeFromCheck(board, (pos[0], i), self):
					a.append((pos[0], i))
			else: 
				break

		for i in range(pos[1] - 1, -1, -1):
			if board[pos[0]][i] == 0:
				if safeFromCheck(board, (pos[0], i), self):
					a.append((pos[0], i))
			else: 
				break

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] + i][pos[1] + i] == 0:
					if safeFromCheck(board, (pos[0] + i, pos[1] + i), self):
						a.append((pos[0] + i, pos[1] + i))
				else: break
			else: break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] - i][pos[1] - i] == 0:
					if safeFromCheck(board, (pos[0] - i, pos[1] - i), self):
						a.append((pos[0] - i, pos[1] - i))
				else: break
			else: break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] - i][pos[1] + i] == 0:
					if safeFromCheck(board, (pos[0] - i, pos[1] + i), self):
						a.append((pos[0] - i, pos[1] + i))
				else: break
			else: break

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] + i][pos[1] - i] == 0:
					if safeFromCheck(board, (pos[0] + i, pos[1] - i), self):
						a.append((pos[0] + i, pos[1] - i))
				else: break
			else: break

		return a

	def isKill(self, pos, board):
		a = []

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] + i][pos[1] + i]:
					if board[pos[0] + i][pos[1] + i].color != self.color:
						if safeFromCheck(board, (pos[0] + i, pos[1] + i), self):
							a.append((pos[0] + i, pos[1] + i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] - i][pos[1] - i]:
					if board[pos[0] - i][pos[1] - i].color != self.color:
						if safeFromCheck(board, (pos[0] - i, pos[1] - i), self):
							a.append((pos[0] - i, pos[1] - i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] - i][pos[1] + i]:
					if board[pos[0] - i][pos[1] + i].color != self.color:
						if safeFromCheck(board, (pos[0] - i, pos[1] + i), self):
							a.append((pos[0] - i, pos[1] + i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] + i][pos[1] - i]:
					if board[pos[0] + i][pos[1] - i].color != self.color:
						if safeFromCheck(board, (pos[0] + i, pos[1] - i), self):
							a.append((pos[0] + i, pos[1] - i))
					break

		for i in range(pos[0] + 1, 8):
			if board[i][pos[1]]:
				if board[i][pos[1]].color != self.color:
					if safeFromCheck(board, (i, pos[1]), self):
						a.append((i, pos[1]))
				break

		for i in range(pos[0] - 1, -1, -1):
			if board[i][pos[1]]:
				if board[i][pos[1]].color != self.color:
					if safeFromCheck(board, (i, pos[1]), self):
						a.append((i, pos[1]))
				break

		for i in range(pos[1] + 1, 8):
			if board[pos[0]][i]:
				if board[pos[0]][i].color != self.color:
					if safeFromCheck(board, (pos[0], i), self):
						a.append((pos[0], i))
				break

		for i in range(pos[1] - 1, -1, -1):
			if board[pos[0]][i]:
				if board[pos[0]][i].color != self.color:
					if safeFromCheck(board, (pos[0], i), self):
						a.append((pos[0], i))
				break
		return a

	def killWays(self, pos, board):
		a = []

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] + i][pos[1] + i] == 0:
					a.append((pos[0] + i, pos[1] + i))
				else: 
					if board[pos[0] + i][pos[1] + i].color != self.color:
						a.append((pos[0] + i, pos[1] + i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] - i][pos[1] - i] == 0:
					a.append((pos[0] - i, pos[1] - i))
				else:
					if board[pos[0] - i][pos[1] - i].color != self.color:
						a.append((pos[0] - i, pos[1] - i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] - i < 8 and 0 <= pos[1] + i < 8:
				if board[pos[0] - i][pos[1] + i] == 0:
					a.append((pos[0] - i, pos[1] + i))
				else:
					if board[pos[0] - i][pos[1] + i].color != self.color:
						a.append((pos[0] - i, pos[1] + i))
					break

		for i in range(1, 8):
			if 0 <= pos[0] + i < 8 and 0 <= pos[1] - i < 8:
				if board[pos[0] + i][pos[1] - i] == 0:
					a.append((pos[0] + i, pos[1] - i))
				else:
					if board[pos[0] + i][pos[1] - i].color != self.color:
						a.append((pos[0] + i, pos[1] - i))
					break

		for i in range(pos[0] + 1, 8):
			if board[i][pos[1]] == 0:
				a.append((i, pos[1]))
			else: 
				if board[i][pos[1]].color != self.color:
					a.append((i, pos[1]))
				break

		for i in range(pos[0] - 1, -1, -1):
			if board[i][pos[1]] == 0:
				a.append((i, pos[1]))
			else: 
				if board[i][pos[1]].color != self.color:
					a.append((i, pos[1]))
				break

		for i in range(pos[1] + 1, 8):
			if board[pos[0]][i] == 0:
				a.append((pos[0], i))
			else: 
				if board[pos[0]][i].color != self.color:
					a.append((pos[0], i))
				break

		for i in range(pos[1] - 1, -1, -1):
			if board[pos[0]][i] == 0:
				a.append((pos[0], i))
			else: 
				if board[pos[0]][i].color != self.color:
					a.append((pos[0], i))
				break

		return a

	def ty(self):
		return "Queen"
