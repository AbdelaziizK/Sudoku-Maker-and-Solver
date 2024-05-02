"""
a program for interacting with  user to use Sudoku puzzle maker and solver.
"""

import Sudoku
import SudokuSolver

print("==== Sudoku ====", "\n")
options = ["get Sudoku", "get solved Sudoku", "get a Sudoku and it's solution", "solve a Sudoku"]

while True:
	for i in range(1, len(options)+1):
		print(i, "-", options[i-1])
	print()
	
	try:
		option = eval(input("Enter the number of option you want: "))
		if option not in [x for x in range(1, len(options)+1)]:
			raise Exception
	except Exception:
		print(option, "is not in option. try number from options.")
	
	print()
	
	if option == 1:
		print(Sudoku.shape(Sudoku.get_sudoku()))
	
	elif option == 2:
		print(Sudoku.shape(Sudoku.get_solved_sudoku()))
	
	elif option == 3:
		sudoku = Sudoku.get_sudoku()
		print('== Sudoku ==')
		print(Sudoku.shape(sudoku))
		print('== Solved ==')
		print(Sudoku.shape(SudokuSolver.solve(sudoku)))
	
	elif option == 4:
		print("-Enter the Sudoku you want to solve;\n-Enter each row (9 elements) in a separate line with One space between them.\
  \n-For hidden numbers use *.\n-(for example: * 5 2 * 3 8 * * 7)\
  \n-Or you can enter(copy) the full game at one time, but one space between each Two numbers and newline after each row:")
		sudoku_list = []
		for i in range(9):
			line = []
			while len(line) < 9:
				try:
					line = input(str(i+1) + " :")
					if len(line.split(' ')) < 9:
						raise Exception
				except SyntaxError:
					print("Enter only One space between elements.")
				except Exception:
					print('length of line you entered isn\'t 9, try again')
				line = line.split(' ')
				for j in range(len(line)):
					if line[j] == '*':
						continue
					line[j] = eval(line[j])
				sudoku_list.append(line)
		
		if SudokuSolver.is_solved(sudoku_list):
			print("There's no hidden numbers to solve in this Sudoku.")
		else:
			print('== Your Sudoku ==')
			print(Sudoku.shape(sudoku_list))
			
			solved_sudoku_list = SudokuSolver.solve(sudoku_list)
			
			print('== Your Sudoku [Solved] ==')
			print(Sudoku.shape(solved_sudoku_list))

