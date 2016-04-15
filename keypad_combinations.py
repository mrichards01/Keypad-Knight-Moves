import time

class Keypad:

	WIDTH = 5
	HEIGHT = 4

	def __init__(self):
		##initialise all keypad values explictly (including nulls)
		self.__keys = {}
		self.__keys[(0,0)] = 'A'
		self.__keys[(0,1)] = 'F'
		self.__keys[(0,2)] = 'K'
		self.__keys[(1,0)] = 'B'
		self.__keys[(1,1)] = 'G'
		self.__keys[(1,2)] = 'L'
		self.__keys[(1,3)] = '1'
		self.__keys[(2,0)] = 'C'
		self.__keys[(2,1)] = 'H'
		self.__keys[(2,2)]= 'M'
		self.__keys[(2,3)] = '2'
		self.__keys[(3,0)]= 'D'
		self.__keys[(3,1)] = 'I'
		self.__keys[(3,2)] = 'N'
		self.__keys[(3,3)] = '3'
		self.__keys[(4,0)] = 'E'
		self.__keys[(4,1)] = 'J'
		self.__keys[(4,2)] = 'O'
		self.__combination_counts = {}

	def is_vowel(self, key_pressed):
		if key_pressed in ['A','O','E','I','U']:
			return True
		return False

	#check to see if the combination has already been computed any count
	def check_preprocessed_count(self, key_pressed, seq_len, vowel_count):
		# collate the 3 parameters with a '_' delimiter
		key = (key_pressed,seq_len,vowel_count)

		if key in self.__combination_counts:
			return self.__combination_counts[key]
		
		return None
	
	def add_processed_count(self, key_pressed, seq_len, vowel_count, no_combinations):
		key = (key_pressed,seq_len,vowel_count)
		if key not in self.__combination_counts:
			self.__combination_counts[key] = no_combinations

	def key_exists(self, x, y):
		#check if the proposed key is one of the blank spots
		if (x, y) in self.__keys:
			return True
		return False

	def get_x_knight_moves(self, x, y, x_offset):
		all_moves = []
		direction = 1
		if x_offset<0:
			direction=-1
		 
		x_offset = x_offset+direction

		for x1 in range (x,x+x_offset,direction):
			if not self.key_exists(x1, y):
				break
			#add potential end moves
			if x1==x+x_offset-direction:
				if self.key_exists(x1,y-1):
					all_moves.append((x1,y-1))
				if self.key_exists(x1,y+1):
					all_moves.append((x1,y+1))
		return all_moves

	def get_y_knight_moves(self, x, y, y_offset):
		all_moves = []
		direction = 1
		if y_offset<0:
			direction=-1
			
		y_offset = y_offset+direction
	
		for y1 in range (y,y+y_offset, direction):
			if not self.key_exists(x, y1):
				break
			#add potential end moves
			if y1==y+y_offset-direction:
				if self.key_exists(x-1,y1):
					all_moves.append((x-1,y1))
				if self.key_exists(x+1,y1):
					all_moves.append((x+1,y1))
		return all_moves

	#function to return all the postions that you could possibly move to in a knight fashion
	def get_all_knight_moves(self,x, y):
		#all keys need to be checed in the knight move to validate the move
		all_moves=[]
		#2 moves vertically up and 2 moves horizontally on either side
		for move in self.get_y_knight_moves(x,y,-2):
			all_moves.append(move)

		#2 moves vertically down and 2 moves horizontally on either side
		for move in self.get_y_knight_moves(x,y,2):
			all_moves.append(move)

		#2 moves horizontally left and 2 moves vertically up or down
		for move in self.get_x_knight_moves(x,y,-2):
			all_moves.append(move)

		#2 moves horizonstally right and 2 moves verically up or down
		for move in self.get_x_knight_moves(x,y,2):
			all_moves.append(move)

		return all_moves

	def find_no_combinations_from_key(self, x, y, current_seq, vowel_count):
		key_pressed = self.__keys[(x,y)]

		## no combinations here or from here onwards if the vowel count exceeds two
		key_is_a_vowel = self.is_vowel(key_pressed) 
		if key_is_a_vowel:
			vowel_count = vowel_count+1
			if vowel_count>2:
				return 0
		
		#if the sequence is 10 keys long, this forms a valid sequence
		new_seq = current_seq+key_pressed
		if (len(new_seq)==10):
			self.add_processed_count(key_pressed, len(new_seq), vowel_count, 1)
			return 1
		
		##otherwise check if there is a cached value 
		combination_count = self.check_preprocessed_count(key_pressed, len(new_seq),vowel_count)
		if combination_count is not None:
			return combination_count

		#otherwise this is a valid prefix
		combination_count = 0
		#check all possible neighbours by a knight move
		neighbour_knight_coords = self.get_all_knight_moves(x, y)
		for move in neighbour_knight_coords:
			neighbour_x = move[0]
			neighbour_y = move[1]
			combination_count = combination_count+self.find_no_combinations_from_key(neighbour_x, neighbour_y, new_seq, vowel_count)
		
		self.add_processed_count(key_pressed, len(new_seq), vowel_count, combination_count)
		
		return combination_count

	def find_all_combinations(self):
		total_combinations = 0
		for x in range (0, Keypad.WIDTH):
			for y in range(0, Keypad.HEIGHT):
				#exceptions for blank key
				if (x,y) in self.__keys:
					total_combinations = total_combinations+my_keypad.find_no_combinations_from_key(x,y,'',0)

		return total_combinations

my_keypad = Keypad()
start_time = time.time()
print my_keypad.find_all_combinations()
print("---  Execution Time: %s seconds ---" % (time.time() - start_time))