
"""
a program makes Sudoku puzzle
"""

import random

def is_sudoku(lst):
	"""
	returns True if the length of the outher list and inner lists is 9,
	and there's no duplicated numbers in rows, columns and 3x3 grids.
	otherwise it raises Exception with descriptive text. and returns False.
	"""
	result = True
	
	if len(lst) != 9:
		raise Exception('Wrong Sudoku. rows are less or more than 9')
		return False
	for i in range(len(lst)):
		if len(lst[i]) != 9:
			raise Exception(f'Wrong Sudoku. row {lst.index(i)} is less or more than 9')
			return False
	
	nums = [x for x in range(1, 10)]
	for i in lst:
		for j in nums:
			if i.count(j) > 1:
				raise Exception(f'Wrong Sudoku. {j} is duplicated in row {lst.index(i) + 1}')
				return False
	
	temp = []
	for j in range(len(lst)):
		for i in range(len(lst)):
			temp.append(lst[i][j])
		for k in nums:
			if temp.count(k) > 1:
				raise Exception(f'Wrong Sudoku. {k} is duplicated in column {j+1}')
				return False
		temp.clear()
	
	temp = []
	for y in range(int(len(lst) / 3)):
		for x in range(int(len(lst) / 3)):
			for i in range(x*3, x*3+1):
				temp.extend(lst[i][y*3 : y*3+3])
			for k in nums:
				if temp.count(k) > 1:
					print(f'Wrong Sudoku. {k} is duplicated in grid {x} {y}')
					return False
			temp.clear()
	
	return result

def valid_numbers(row, column, lst):
	"""
	returns a list of numbers that arn't in the row and column and 3×3 grid
	of postion lst[row][column]
	"""
	
	valid_nums = set([x for x in range(1, 10)])
	valid_nums = valid_nums.difference(lst[row])
	for i in range(len(lst)):
		if lst[i][column] in valid_nums:
			valid_nums.remove(lst[i][column])
	x, y = grid_coordinates(row, column)
	
	for i in range((x-1)*3, (x-1)*3+3):
		valid_nums = valid_nums.difference(lst[i][(y-1)*3: (y-1)*3+3])
	valid_nums = list(valid_nums)
	random.shuffle(valid_nums)
	
	return valid_nums

def grid_coordinates(row, column):
	"""
	returns the x and y of the square contains list[row][column],
	for example x = 1 for first 3 rows or y = 3 for columns from 6 to 8
	"""
	x, y = 0, 0
	if 9 / (row+1) >= 3:
		x = 1
	elif 9 / (row+1) >= 1.5:
		x = 2
	else:
		x = 3

	if 9 / (column+1) >= 3:
		y = 1
	elif 9 / (column+1) >= 1.5:
		y = 2
	else:
		y = 3
	
	return x, y

def hide_numbers(lst):
	"""
	randomly hides 3 to 6 random numbers in each 3x3 grid
	"""
	for j in range(int(len(lst) / 3)):
		for i in range(int(len(lst) / 3)):
			# calculates r (row) and c (column) to acces each grid's elements
			r = i * 3
			c = j * 3
			number_of_missing_numbers = random.randint(3, 6)
			missing_numbers = random.sample(list(range(1, 10)), k=number_of_missing_numbers)
			for k in range(len(lst)):
				if k % 3 == 0 and k != 0:
					r += 1
					c -= 3
				# if current element in the missing numbers, replace it with '*'
				if lst[r][c] in missing_numbers:
					lst[r][c] = '*'
				c += 1
	return lst

def shape(lst = None):
	"""
	returns a structured Sudoku in a nice looking shape
	"""
	if lst == None:
		lst == get_sudoku()
	list_to_show = ''
	for i in range(len(lst)):
		for j in range(len(lst[i])):
			if j % 3 == 0:
				list_to_show += " "
			list_to_show += format(str(lst[i][j]), "^3s")
		if (i+1) % 3 == 0 and (i+1) != 9:
			list_to_show += '\n'
		list_to_show += '\n'
	return list_to_show

def get_solved_sudoku():
	"""
	makes the Sudoku table, hides some numbers and returns it
	"""
	nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	solved_sudoku = [[None for x in range(9)] for y in range(9)]
	
	for i in solved_sudoku:
		while None in i:
			valid_nums = valid_numbers(solved_sudoku.index(i), i.index(None), solved_sudoku)
			# if cant find valud numbers to add, clears the row and refill it again
			if len(valid_nums) == 0:
				i.clear()
				i.extend([None for x in range(9)])
			for j in valid_nums:
				i.insert(i.index(None), j)
				i.remove(None)
				break
	return solved_sudoku

def get_sudoku():
	"""
	returns a solved Sudoku (without hidden numbers)
	"""
	sudoku = get_solved_sudoku()
	sudoku = hide_numbers(sudoku)
	return sudoku
