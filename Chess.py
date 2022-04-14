import pygame as pg
import copy
from Piece import *


class Board:
	def __init__(self, screen, res, cell_colors, way_radius, wait_screen_color):
		self.screen = screen
		self.cell_colors = cell_colors
		self.wait_screen_color = wait_screen_color
		self.way_radius = way_radius
		self.cell_width = int(res[0]/8)
		self.cell_height = int(res[1]/8)
		self.is_get_Piece = 0
		self.is_was_up = 0
		self.start_piece_position = (0, 0)
		self.moving = 0
		self.possible_ways = []
		self.order = 'w'

		self.cells = [[0 for j in range(8)] for i in range(8)]

		self.startArrangement()

		
	def drawBoard(self):
		for i in range(8):
			for j in range(8):
				if (i + j) % 2 != 0:
					pg.draw.rect(self.screen, self.cell_colors[1], (i * self.cell_width, j * self.cell_height, self.cell_width, self.cell_height))
				else:
					pg.draw.rect(self.screen, self.cell_colors[0], (i * self.cell_width, j * self.cell_height, self.cell_width, self.cell_height))

	def drawPieces(self):
		for i in range(8):
			for j in range(8):
				if self.cells[i][j]:
					self.screen.blit(self.cells[i][j].img, (i * self.cell_width, j * self.cell_height, self.cell_width, self.cell_height))

	def startArrangement(self):
		self.cells[0][0] = Rock('b', (self.cell_width, self.cell_height))
		self.cells[1][0] = Knight('b', (self.cell_width, self.cell_height))
		self.cells[2][0] = Bishop('b', (self.cell_width, self.cell_height))
		self.cells[3][0] = Queen('b', (self.cell_width, self.cell_height))
		self.cells[4][0] = King('b', (self.cell_width, self.cell_height))
		self.cells[5][0] = Bishop('b', (self.cell_width, self.cell_height))
		self.cells[6][0] = Knight('b', (self.cell_width, self.cell_height))
		self.cells[7][0] = Rock('b', (self.cell_width, self.cell_height))

		for i in range(8):
			self.cells[i][1] = Pawn('b', (self.cell_width, self.cell_height))


		self.cells[0][7] = Rock('w', (self.cell_width, self.cell_height))
		self.cells[1][7] = Knight('w', (self.cell_width, self.cell_height))
		self.cells[2][7] = Bishop('w', (self.cell_width, self.cell_height))
		self.cells[3][7] = Queen('w', (self.cell_width, self.cell_height))
		self.cells[4][7] = King('w', (self.cell_width, self.cell_height))
		self.cells[5][7] = Bishop('w', (self.cell_width, self.cell_height))
		self.cells[6][7] = Knight('w', (self.cell_width, self.cell_height))
		self.cells[7][7] = Rock('w', (self.cell_width, self.cell_height))

		for i in range(8):
			self.cells[i][6] = Pawn('w', (self.cell_width, self.cell_height));

	def drawWays(self):
		if self.moving:
			w = self.moving.isStep(self.start_piece_position, self.cells)

			if self.moving.ty() == "King":
				p = self.moving.isCastling(self.start_piece_position, self.cells)
				if p[0]:
					w.append((self.start_piece_position[0] - 2, self.start_piece_position[1]))
				if p[1]:
					w.append((self.start_piece_position[0] + 2, self.start_piece_position[1]))

			self.possible_ways.extend(copy.copy(w))
	
			for i in w:
				x, y = i[0] * self.cell_width + self.cell_width // 2, i[1] * self.cell_height + self.cell_height // 2
				pg.draw.circle(self.screen, (100, 255, 100), (x, y), self.way_radius)

	def drawKills(self):
		if self.moving:
			w = self.moving.isKill(self.start_piece_position, self.cells)
			self.possible_ways.extend(copy.copy(w))

			for i in w:
				x, y = i[0] * self.cell_width + self.cell_width // 2, i[1] * self.cell_height + self.cell_height // 2
				pg.draw.circle(self.screen, (255, 100, 100), (x, y), self.way_radius)

	def clearWays(self):
		self.possible_ways = []

	def isWin(self):
		w = []
		t = False
		if self.moving:
			self.cells[self.start_piece_position[0]][self.start_piece_position[1]] = self.moving
			t = True

		for i in range(8):
			for j in range(8):
				if self.cells[i][j]:
					if self.cells[i][j].color == self.order:
						fig = copy.copy(self.cells[i][j])
						self.cells[i][j] = 0
						w.extend(fig.isStep((i, j), self.cells))
						w.extend(fig.isKill((i, j), self.cells))
						self.cells[i][j] = copy.copy(fig)

		if t:
			self.moving = self.cells[self.start_piece_position[0]][self.start_piece_position[1]]
			self.cells[self.start_piece_position[0]][self.start_piece_position[1]] = 0

		if len(w) == 0:
			print("Black win" if self.order == 'w' else "White win")
			exit()

	def makeCastling(self, num, figure):
		if figure.color == 'w':
			if num == 2:
				self.cells[5][7] = copy.copy(self.cells[7][7])
				self.cells[7][7] = 0
			else:
				self.cells[3][7] = copy.copy(self.cells[0][7])
				self.cells[0][7] = 0
		else:
			if num == 2:
				self.cells[5][0] = copy.copy(self.cells[7][0])
				self.cells[7][0] = 0
			else:
				self.cells[3][0] = copy.copy(self.cells[0][0])
				self.cells[0][0] = 0

	def control(self):
		pressed = pg.mouse.get_pressed()
		pos = pg.mouse.get_pos()
		x, y = pos[0] // self.cell_width, pos[1] // self.cell_height

		is_piece = 1 if self.cells[x][y] else 0

		if self.is_get_Piece == 1:
			self.screen.blit(self.moving.img, (pos[0] - self.cell_width//2, pos[1] - self.cell_height//2, self.cell_width, self.cell_height))

		if self.is_was_up == pressed[0] == 1:
			return

		if pressed[0] and self.is_get_Piece == 0 and is_piece and self.order == self.cells[x][y].color:
			self.is_get_Piece = 1
			self.moving = self.cells[x][y]
			self.cells[x][y] = 0
			self.start_piece_position = (x, y)

		elif pressed[0] and self.is_get_Piece == 1:
			if self.start_piece_position[0] == x and self.start_piece_position[1] == y:
				self.cells[x][y] = self.moving
				self.moving = 0
				self.is_get_Piece = 0

			if (x, y) in self.possible_ways:
				if not is_piece:
					self.cells[x][y] = self.moving

					if self.cells[x][y].is_first == True and self.cells[x][y].ty() == "King":
						if self.start_piece_position[0] + 2 == x and self.start_piece_position[1] == y:
							self.makeCastling(2, self.cells[x][y])
						if self.start_piece_position[0] - 2 == x and self.start_piece_position[1] == y:
							self.makeCastling(-2, self.cells[x][y])


					if self.cells[x][self.start_piece_position[1]]:
						if self.cells[x][self.start_piece_position[1]].ty() == "Pawn":
							if self.cells[x][self.start_piece_position[1]].is_ghost:
								self.cells[x][self.start_piece_position[1]] = 0


					self.cells[x][y].is_first = False
					self.moving = 0
					self.is_get_Piece = 0
					self.order = 'b' if self.order == 'w' else 'w'

				elif self.cells[x][y].color != self.moving.color and (x, y) in self.possible_ways:
					self.cells[x][y] = self.moving
					self.cells[x][y].is_first = False
					self.moving = 0
					self.is_get_Piece = 0
					self.order = 'b' if self.order == 'w' else 'w'

			for i in range(8):
					for j in range(8):
						if self.cells[i][j]:
							if self.cells[i][j].ty() == "Pawn":
								if not self.cells[i][j].is_first and self.cells[i][j].color == self.order and self.cells[i][j].is_ghost:
									self.cells[i][j].is_ghost = False


		self.is_was_up = 1 if pressed[0] else 0

	def isPawnKing(self):
		for i in range(8):
			for j in (0, 7):
				if self.cells[i][j]:
					if self.cells[i][j].ty() == "Pawn":
						return (i, j)
		return False

	def makeChoise(self, figure_position):
		pressed = pg.mouse.get_pressed()
		pos = pg.mouse.get_pos()
		x, y = pos[0] // self.cell_width, pos[1] // self.cell_height

		pg.draw.rect(self.screen, self.wait_screen_color, (0 * self.cell_width, 1 * self.cell_height, self.cell_width * 8, self.cell_height * 6))
		choises = (Rock('w' if self.order == 'b' else 'b', (self.cell_width * 2, self.cell_height * 2)), Knight('w' if self.order == 'b' else 'b', (self.cell_width * 2, self.cell_height * 2)), 
				   Bishop('w' if self.order == 'b' else 'b', (self.cell_width * 2, self.cell_height * 2)), Queen('w' if self.order == 'b' else 'b', (self.cell_width * 2, self.cell_height * 2)))
		positions = ((1.5, 1.5), (4.5, 1.5), (1.5, 4.5), (4.5, 4.5))

		for i in range(4):
			self.screen.blit(choises[i].img, (positions[i][0] * self.cell_width, positions[i][1] * self.cell_height, self.cell_width * 2, self.cell_height * 2))


		if pressed[0]:
			if 1 <= x <= 3 and 1 <= y <= 3:
				self.cells[figure_position[0]][figure_position[1]] = Rock('w' if self.order == 'b' else 'b', (self.cell_width, self.cell_height))

			if 4 <= x <= 6 and 1 <= y <= 3:
				self.cells[figure_position[0]][figure_position[1]] = Knight('w' if self.order == 'b' else 'b', (self.cell_width, self.cell_height))

			if 1 <= x <= 3 and 4 <= y <= 6:
				self.cells[figure_position[0]][figure_position[1]] = Bishop('w' if self.order == 'b' else 'b', (self.cell_width, self.cell_height))

			if 4 <= x <= 6 and 4 <= y <= 6:
				self.cells[figure_position[0]][figure_position[1]] = Queen('w' if self.order == 'b' else 'b', (self.cell_width, self.cell_height))




class App:
	def __init__(self, res, cell_colors, way_radius, wait_screen_color):
		self.screen = pg.display.set_mode(res)
		self.board = Board(self.screen, res, cell_colors, way_radius, wait_screen_color)

	def run(self):
		while True:
			self.screen.fill('black')

			self.board.drawBoard()
			self.board.drawPieces()

			pos = self.board.isPawnKing()
			if pos:
				self.board.makeChoise(pos)
			else:
				self.board.isWin()
				self.board.control()
				self.board.clearWays()
				self.board.drawWays()
				self.board.drawKills()

			pg.display.update()
			[exit() for i in pg.event.get() if i.type == pg.QUIT]


if __name__ == '__main__':
	res = (640, 640)
	cell_colors = ((150, 150, 150), (100, 100, 100))
	wait_screen_color = (125, 125, 125)
	way_radius = 10

	app = App(res, cell_colors, way_radius, wait_screen_color)
	app.run()
