import time

class Keypad:

	WIDTH = 5
	HEIGHT = 4

	def __init__(self):
		##initialise all keypad values explictly
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
		return (key_pressed.upper() in ['A','O','E','I','U'])

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

	#method to rturn if a move if valid , given the axis and number of steps to be taken in a direction
	def is_move_valid(self, x, y, axis, steps):
		all_moves = []

		#validate if each key exists on the keypad
		if axis=='x':
			x = x+steps
		elif axis=='y':
			y = y+steps
		else:
			raise ValueError("Move is not valid, only 'x' or 'y' are valid axis", axis)

		if (x,y) not in self.__keys:
				return False
		return True

	def add_move_if_valid(self, all_moves, x, y, axis, steps):
		if self.is_move_valid(x, y, axis, steps):
			if axis=='x':
				all_moves.append((x+steps, y))
			if axis=='y':
				all_moves.append((x, y+steps))
	
	#function to return all the postions that you could possibly move to in a knight fashion
	def get_all_knight_moves(self, pos):
		x = pos[0]
		y = pos[1]
		#all keys need to be checked in the knight move to validate the move
		all_moves=[]
		# total of 8 different moves
		if self.is_move_valid(x, y, 'x', -2):
			self.add_move_if_valid(all_moves, x-2, y, 'y', -1)
			self.add_move_if_valid(all_moves, x-2, y, 'y', 1)
			
		if self.is_move_valid(x, y, 'x', 2):
			self.add_move_if_valid(all_moves, x+2, y, 'y', -1)
			self.add_move_if_valid(all_moves, x+2, y, 'y', 1)


		if self.is_move_valid(x, y, 'y',-2):
			self.add_move_if_valid(all_moves, x, y-2, 'x', -1)
			self.add_move_if_valid(all_moves, x, y-2, 'x', 1)

		if self.is_move_valid(x, y, 'y',2):
			self.add_move_if_valid(all_moves, x, y+2, 'x', -1)
			self.add_move_if_valid(all_moves, x, y+2, 'x', 1)

		return all_moves

	def find_no_combinations_from_key(self, pos, current_seq, vowel_count):
		key_pressed = self.__keys[pos]

		# no of combinations is 0 if the vowel count exceeds two in the current given string
		key_is_a_vowel = self.is_vowel(key_pressed) 
		if key_is_a_vowel:
			vowel_count +=1
			if vowel_count>2:
				return 0
		
		# if the sequence is 10 keys long, this forms a valid sequence
		new_seq = current_seq+key_pressed
		if len(new_seq)==10:
			# add to cache the vowel count
			self.add_processed_count(key_pressed, len(new_seq), vowel_count, 1)
			return 1
		
		# otherwise check if there is a cached value 
		combination_count = self.check_preprocessed_count(key_pressed, len(new_seq),vowel_count)
		if combination_count is not None:
			return combination_count

		# otherwise this is a valid prefix, with no cache value
		combination_count = 0
		# check all possible neighbours by a knight move
		neighbour_knight_coords = self.get_all_knight_moves(pos)
		for move in neighbour_knight_coords:
			combination_count +=self.find_no_combinations_from_key(move, new_seq, vowel_count)

		# add to cache after finding the number of combinations from a given prefix
		self.add_processed_count(key_pressed, len(new_seq), vowel_count, combination_count)
		
		return combination_count

	def find_all_combinations(self):
		total_combinations = 0
		for x in range (0, Keypad.WIDTH):
			for y in range(0, Keypad.HEIGHT):
				# where there is a valid key for this position
				if (x,y) in self.__keys:
					total_combinations +=my_keypad.find_no_combinations_from_key((x,y),'',0)

		return total_combinations

my_keypad = Keypad()
start_time = time.time()
print ("Total combinations: %s" % my_keypad.find_all_combinations())
print("---  Execution Time: %s seconds ---" % (time.time() - start_time))