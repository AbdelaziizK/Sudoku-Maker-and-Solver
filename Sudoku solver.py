
"""
a program to solve Sudoku puzzle
"""

import random
import copy
import Sudoku

def is_solved(lst):
	"""
	returns True if there's no hidden numbers in the Sudoku. otherwise returns False.
	it's not for checking it's True or not.
	"""
	result = True
	for i in lst:
		if i.count('*') > 0:
			result = False
			break
	return result

def is_true(lst):
	"""
	returns True if there's no duplicated number in a row or a column or a 3x3 grid.
	otherwise it returns False.
	"""
	result = True
	for i in range(len(lst)):
		for j in range(len(lst[i])):
			if lst[i][j] == "*":
				return False
			if len(Sudoku.valid_numbers(i, j, lst)) > 0:
				return False
	return result

def number_of_hiddens(lst):
	"""
	returns the number of hidden numbers in all Sudoku table
	"""
	num_of_hidden_nums = 0
	for i in lst:
		num_of_hidden_nums += i.count('*')
	return num_of_hidden_nums

def exists_in_different_rows_in_horizontal_grids(num, row, column, lst):
	"""
	it returns True if the two horizontal grids to the current element
	contain the same number it's trying to add in different rows
	"""
	x, y = Sudoku.grid_coordinates(row, column)
	result = 0
	
	for i in range((x-1)*3, (x-1)*3+3):
		for j in range(int(len(lst[i])/3)):
			r = i
			c = j * 3
			if r == row and j == y - 1:
				if lst[r][c : c+3].count('*') >= 2:
					for x in range(len(lst[r][c : c+3])):
						if lst[r][c+x] == '*':
							if c+x == column:
								continue
							if num in Sudoku.valid_numbers(r,c+x, lst):
								result -= 1
							else:
								pass
			if r == row or j == y - 1:
				continue
			if num in lst[r][c : c+3]:
				result += 1
			
	if result == 2:
		return True
	return False

def exists_in_different_columns_in_vertical_grids(num, row, column, lst):
	"""
	returns True if the two vertical grid to the current element contain
	the same number it's trying to add in different columns
	"""
	
	x, y = Sudoku.grid_coordinates(row, column)
	result = 0
	
	for i in range(int(len(lst[0]) / 3)):
		for j in range((y-1)*3, (y-1)*3+3):
			for k in range(3):
				r = i * 3 + k
				c = j
				if c == column  and i == x - 1:
					if r == row:
						continue
					if lst[r][c] == '*':
						if num in Sudoku.valid_numbers(r, c, lst):
							result -= 1
						else:
							pass
				if c == column:
					continue
				if num == lst[r][c]:
					result += 1
	if result == 2:
		return True
	return False

def solve(lst):
	"""
	solves the Sudoku by looping it to finds positions of hidden numbers,
	and finds valid numbers can be placed in its position, if there's only One valid number,
	it raplaces it right away, if more than One, it tries them,
	if a number doesn't oppose the roles of the game, it replaces hidden number by it,
	leading to decrease the posibilities of numbers are valid to replaced the hidden number.
	variables for comparing the numbers of hidden numbers before and after solving is used.
	if hidden number before iteration of solve and after are the same,
	it tries one of valid numbers.
	of one hidden positions at a time and saves all positions of hidden positions currently,
	if after solving, it causes to wrong solution,
	it come back and removes the modifications and try another One of that position's valid numbers
	until it leads to completely solving it.
	"""
	try:
		Sudoku.is_sudoku(lst)
	except Exception as e:
		print(e)
		return
		
	modifications = []
	while not is_solved(lst):
		number_of_hiddens_before_solve = number_of_hiddens(lst)
		
		for i in range(len(lst)):
			for j in range(len(lst[i])):
				if lst[i][j] == '*':
					valid_nums = Sudoku.valid_numbers(i, j, lst)
					
					if len(valid_nums) == 1:
						lst[i][j] = valid_nums[0]
						continue
					
					elif len(valid_nums) > 1:
						for k in valid_nums:
							# if this number is found in other two rows but
							#in different grids, it can be added
							
							if exists_in_different_rows_in_horizontal_grids(k ,i ,j ,lst):
								lst[i][j] = k
								break
							
							# if this number is found in other two columns but
							#in different grids, it can be added
							if exists_in_different_columns_in_vertical_grids(k ,i ,j ,lst):
								lst[i][j] = k
								break
					else:
						pass
						
		number_of_hiddens_after_solve = number_of_hiddens(lst)
		
		if number_of_hiddens_before_solve == \
		number_of_hiddens_after_solve\
		and not is_solved(lst):
			modifications.append([])
			for i in range(len(lst)):
				for j in range(len(lst[i])):
					if lst[i][j] == '*':
						modifications[len(modifications)-1].\
						append((i, j))
			valid_nums_for_num_to_add = Sudoku.valid_numbers\
			(modifications[len(modifications)-1][0][0]\
			,modifications[len(modifications)-1][0][1]\
			,lst)
			valid_num_used_as_sol = 0
			for k in valid_nums_for_num_to_add:
				valid_num_used_as_sol = k
				lst[modifications[len(modifications)-1][0][0]]\
				[modifications[len(modifications)-1][0][1]] = k
			modifications[len(modifications)-1].insert(0, valid_num_used_as_sol)
			
		if is_solved(lst):
			if not is_true(lst):
				for i in modifications[len(modifications)-1]:
					valid_nums_for_num_added =\
					Sudoku.valid_numbers(i[1][0], i[1][1], lst)
					for k in valid_nums_for_num_added:
						if i[0] != k:
							lst[i[1][0]][i[1][1]] = k
							i[0] = k
	return lst

