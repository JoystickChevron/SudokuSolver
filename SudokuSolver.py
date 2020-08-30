import pygame;
WIDTH: int = 729;
HEIGHT: int = 810;
SIZE: int = 81;
BLACK = (0,0,0);
BLUE = (0,0,255);
GREEN = (0,255,0);
WHITE = (255,255,255);
AMT = 81;
VALIDKEYS = (pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8, pygame.K_9);

realboard = [[5,3,4,6,7,2,1,9,8],[6,7,8,1,9,5,3,4,2],[9,1,2,3,4,8,5,6,7],[8,5,9,4,2,6,7,1,3],[7,6,1,8,5,3,9,2,4],[4,2,3,7,9,1,8,5,6],[9,6,1,2,8,7,3,4,5],[5,3,7,4,1,9,2,8,6],[2,8,4,6,3,5,1,7,9]];
realboard2 = [[5,3,-1,6,-1,-1,-1,9,8],[-1,7,-1,1,9,5,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,6,-1],[8,-1,-1,4,-1,-1,7,-1,-1],[-1,6,-1,8,-1,3,-1,2,-1],[-1,-1,3,-1,-1,1,-1,-1,6],[-1,6,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,4,1,9,-1,8,-1],[2,8,-1,-1,-1,5,-1,7,9]];
extreme = [[-1,-1,1,-1,-1,-1,8,4,-1],[-1,-1,-1,-1,1,-1,6,-1,-1],[7,-1,-1,4,8,5,-1,3,-1],[5,-1,-1,-1,-1,3,-1,-1,-1],[1,9,-1,5,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,6,5,-1,-1],[-1,5,9,1,8,-1,3,-1,-1],[3,-1,-1,7,2,-1,-1,-1,-1],[6,4,-1,-1,-1,3,-1,-1,-1]];

class Cell:
	def __init__(self, number, region,i,j, missingNeighborI = 0, missingNeighborR = 0):
		self.region = region;
		self.number = number;
		self.i = i;
		self.j = j;
		self.missingNeighborR = missingNeighborR;
		self.missingNeighborI = missingNeighborI;
		self.rectangle = pygame.Rect(self.i, self.j,  AMT, AMT);
		if self.number != -1:
			self.clue = True;
		else:
			self.clue = False;
		
	def __str__(self):
		return str(self.number);
	def __repr__(self):
		return str(self.number);
	def __eq__(self, other) : 
		return self.number == other.number;
	def __hash__(self) : 
		return self.number;
	def draw(self, screen, color, number = None):
		if number == None:
			number = self.number;
		pygame.draw.rect(screen, color, self.rectangle, 1);
		if number == -1 or number ==10:
			numberText = '     ';
			
		else:
			numberText = str(number);
		if self.clue:
			color = GREEN
		text = font.render(numberText, True, color, WHITE);
		textRect = text.get_rect()  
		textRect.center = (self.i + AMT//2, self.j + AMT//2) 
		screen.blit(text, textRect);


class Sudoku:
	def __init__(self, board):
		self.board = board;
		self.cellBoard = [];
		self.prevR = 0;
		self.prevI = 0;
		numcounter = 0;
		j = 0;
		i = 0;
		for region in range(len(self.board)):
			regionArray = [];
			if region <= 2:
				j = 0;
			if 3 <= region <= 5 :
				j = AMT*3;
			if region >= 6:
				j = AMT*6;
			if region == 0 or region == 3 or region == 6:
				i = 0
			if region == 1 or region == 4 or region == 7:
				i = AMT*3;	
			if region == 2 or region == 5 or region == 8:
				i = AMT*6;
			local = i;
			for index in range(len(self.board[region])):	
				cell = Cell(self.board[region][index],region, i, j);
				regionArray.append(cell);
				numcounter += 1;
				i += AMT;
				if numcounter == 3:
					numcounter = 0;
					i = local;
					j += AMT;
			self.cellBoard.append(regionArray);
			
	def getBoard(self):
		return self.cellBoard;
		
	def solve(self):
		while not self.solved():
			for region in range(len(self.cellBoard)):
				for index in range(len((self.cellBoard[region]))):
					if self.cellBoard[region][index].number == -1 or not self.cellBoard[region][index].clue :		
						self.cellBoard[region][index].missingNeighborI = self.prevI;
						self.cellBoard[region][index].missingNeighborR = self.prevR;
						self.changeNumber(index,region,1 );
						self.prevR = region
						self.prevI = index;
		print('Solved!');
	
	def changeNumber(self,index,region,number = 1):
		if number > 9:
			self.cellBoard[region][index].number = -1; #leave current cell blank
			prevRegion = self.cellBoard[region][index].missingNeighborR;
			prevIndex = self.cellBoard[region][index].missingNeighborI;
			newNum = self.cellBoard[prevRegion][prevIndex].number + 1
			self.cellBoard[region][index].draw(screen, BLUE, number);
			self.changeNumber(prevIndex, prevRegion, newNum);
			self.changeNumber(index, region, 1);
		elif not self.isNumberValid(number, region, index):	
			pygame.event.pump();		
			pygame.display.update();	
			self.cellBoard[region][index].draw(screen, BLUE, number);
			number+=1;
			self.changeNumber(index, region, number);
		else:
			self.cellBoard[region][index].number = number;
			self.cellBoard[region][index].draw(screen, BLUE, number);

	def solved(self):
		if not self.evaluate():
			return False;
		wholeBoard = [];
		for region in self.cellBoard:
			wholeBoard += region;
		removedSpaces = [n for n in wholeBoard if n.number != -1];
		return len(removedSpaces) == len(wholeBoard);
	
	def isNumberValid(self, currentNumber, region, index):
		if not (self.evaluateRegion(self.cellBoard[region], currentNumber)):
			return False;
		if not self.evaluateNumber(index, region, currentNumber):	
			return False;		
		return True;
		
	def evaluate(self): #is it a valid board?
		for region in self.cellBoard:
			if not (self.evaluateRegion(region)):
				return False;
		for region in range(len(self.cellBoard)):
			for index in range(len((self.cellBoard[region]))):
				if not self.evaluateNumber(index, region):		
					return False;		
		return True;
		
	def evaluateRegion(self,region, currentNumber = None):
		regionNoSpaces = [num.number for num in region if num.number != -1];
		if currentNumber:
			return currentNumber not in (set(regionNoSpaces));
		return len(set(regionNoSpaces)) == len(regionNoSpaces);

	def evaluateNumber(self, index, region, currentNumber = None):		
		column = [];
		row = [];
		if region == 0 or region == 3 or region == 6:
			regionsToCheckDown = [0,3,6];
		elif region == 1 or region == 4 or region == 7:
			regionsToCheckDown = [1,4,7];
		else:
			regionsToCheckDown = [2,5,8];	
		if region == 0 or region == 1 or region == 2:
			regionsToCheckRight = [0,1,2];
		elif region == 3 or region == 4 or region == 5:
			regionsToCheckRight = [3,4,5];
		else:
			regionsToCheckRight = [6,7,8];
		if index == 0 or index == 3 or index == 6:
			indexesToCheckDown = [0,3,6];
		elif index == 1 or index == 4 or index == 7:
			indexesToCheckDown = [1,4,7];
		else:
			indexesToCheckDown = [2,5,8];	
		if index == 0 or index == 1 or index == 2:
			indexesToCheckRight = [0,1,2];
		elif index == 3 or index == 4 or index == 5:
			indexesToCheckRight = [3,4,5];
		else:
			indexesToCheckRight = [6,7,8];	
		for region in regionsToCheckDown:
			for index in indexesToCheckDown:
				if self.cellBoard[region][index].number != -1:
					column.append(self.cellBoard[region][index]);
		for region in regionsToCheckRight:
			for index in indexesToCheckRight:
				if self.cellBoard[region][index].number != -1:
					row.append(self.cellBoard[region][index]);	
		row = [num.number for num in row if num.number != -1];
		column = [num.number for num in column if num.number != -1];
		if currentNumber is not None:
			return currentNumber not in row and currentNumber not in column;
		return len(set(row)) == len(row) and len(set(column)) == len(column);
	
	def drawBoard(self,screen):
		for region in range(len(self.cellBoard)):
			for index in range(len(self.cellBoard[region])):	
				self.cellBoard[region][index].draw(screen, BLACK);
				pygame.event.pump();		
		pygame.display.update();	
		
	def setNumber(self, index, region, number):
		if number == 0:
			self.cellBoard[region][index].number = -1;
			self.cellBoard[region][index].clue = False;
		else:	
			if self.isNumberValid(number, region, index):
				self.cellBoard[region][index].number = number;
				self.cellBoard[region][index].clue = True;
				
				

x = Sudoku(extreme);
pygame.init();
clock = pygame.time.Clock();
font = pygame.font.Font('freesansbold.ttf', 32) 
screen = pygame.display.set_mode((WIDTH,HEIGHT));
screen.fill(WHITE);

while True:
	events = pygame.event.get();
	cellBoard = x.getBoard();
	pressed1, pressed2, pressed3 = pygame.mouse.get_pressed();		
	if pressed1:
		pos = pygame.mouse.get_pos()
		for region in range(len(cellBoard)):
			for index in range(len((cellBoard[region]))):
				if cellBoard[region][index].rectangle.collidepoint(pos):
					for event in events:
						if event.type == pygame.KEYDOWN:
							if event.key in VALIDKEYS:
								x.setNumber(index,region,event.key-48);
							if event.key == pygame.K_0:
								x.setNumber(index,region,0);
							if event.key == pygame.K_SPACE:
								x.solve();				
	x.drawBoard(screen);
	pygame.event.pump();	