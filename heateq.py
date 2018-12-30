import numpy as np
import pygame


# Important class definitions

class Cell:

	def __init__(self, grid, inx, iny, left, top, dx, h, bordercell, temp=0):

		self.grid = grid
		self.inx = inx
		self.iny = iny
		self.left = left
		self.top = top
		self.dx = dx
		self.h = h
		self.temp = temp
		self.bordercell = bordercell

		self.new_temp = self.temp
		self.neighbors = []

	def set_neighbors(self):
		if not self.bordercell:
			self.neighbors.append(self.grid.cells[self.iny][self.inx-1])
			self.neighbors.append(self.grid.cells[self.iny][self.inx+1])
			self.neighbors.append(self.grid.cells[self.iny-1][self.inx])
			self.neighbors.append(self.grid.cells[self.iny+1][self.inx])


	def curvaturex(self):
		return ( self.neighbors[1].temp - 2*self.temp + self.neighbors[0].temp )/(self.dx**2)

	def curvaturey(self):
		return ( self.neighbors[3].temp - 2*self.temp + self.neighbors[2].temp )/(self.dx**2)

	def calculate_new_temp(self):
		if self.bordercell:
			pass
		else:
			self.new_temp = self.temp + self.h*(self.curvaturex() + self.curvaturey())

	def set_new_temp(self):
		self.temp = self.new_temp

	def heat(self):
		self.temp = self.temp + 1000

	def cool(self):
		self.temp = self.temp - 1000

			
class Grid:

	def __init__(self):
		self.cells = []



pygame.init()

# Discretization step size (px)
dx = 4
h = 1

# Number of discretization steps in x and y directions
Nx = 70
Ny = 70


disp_width = Nx*dx
disp_height = Ny*dx
FPS = 60





display = pygame.display.set_mode((disp_width, disp_height))
surface = pygame.Surface((disp_width, disp_height))
# pxarray = pygame.PixelArray(surface)
pygame.display.set_caption("Heat Equation Solver")
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)



def initialize():
	global grid

	grid = Grid()

	px = 0
	inx = 0
	py = 0
	iny = 0

	while py+dx<=disp_height:
		grid.cells.append([])
		while px+dx<=disp_width:
			border_boolean = (px==0 or py==0 or abs(px+dx-disp_width)<0.5 or abs(py+dx-disp_height)<0.5)
			grid.cells[iny].append(Cell(grid, inx, iny, px, py, dx, h, border_boolean))
			inx = inx+1
			px = px+dx
		iny = iny+1
		py = py+dx
		inx, px = 0, 0

	# print(grid.cells)

	for i in range(len(grid.cells)):
		for j in range(len(grid.cells[i])):
			grid.cells[i][j].set_neighbors()
	
def heat_cell(x, y):
	grid.cells[y//dx][x//dx].heat()

def cool_cell(x, y):
	grid.cells[y//dx][x//dx].cool()

def update():

	for i in range(len(grid.cells)):
		for j in range(len(grid.cells[i])):
			grid.cells[i][j].calculate_new_temp()

	for i in range(len(grid.cells)):
		for j in range(len(grid.cells[i])):
			grid.cells[i][j].set_new_temp()

def draw():

	for i in range(len(grid.cells)):
		for cell in grid.cells[i]:
			if cell.temp>0:
				pygame.draw.rect(surface, (min(cell.temp, 255), min(255*(1/(np.exp(-(cell.temp-400)/50)+1)), 255), min(255*(1/(np.exp(-(cell.temp-800)/100)+1)), 255)), (cell.left, cell.top, dx, dx))
			else:
				pygame.draw.rect(surface, (0, 0, min(abs(cell.temp), 255)), (cell.left, cell.top, dx, dx))





def mainloop():
	global heating_on

	running = True
	heating_on = False
	cooling_on = False
	initialize()

	while running:
		for event in pygame.event.get():
			# print(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				(btn1, btn2, btn3) = pygame.mouse.get_pressed()
				if btn1:
					heating_on = True
				if btn3:
					cooling_on = True

			if event.type == pygame.MOUSEBUTTONUP:
				(btn1, btn2, btn3) = pygame.mouse.get_pressed()
				if not btn1:
					heating_on = False
				if not btn3:
					cooling_on = False

		if heating_on:
			(x, y) = pygame.mouse.get_pos()
			heat_cell(x, y)
		if cooling_on:
			(x, y) = pygame.mouse.get_pos()
			cool_cell(x, y)

		update()

		draw()

		display.blit(surface, (0,0))
		pygame.display.update()



mainloop()


