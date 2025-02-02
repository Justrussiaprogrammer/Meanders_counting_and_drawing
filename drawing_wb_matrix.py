from tkinter import *
import functions

current_height = 800
current_width = 800

root = Tk()
C = Canvas(root, bg="white", height=current_height, width=current_width)

mass = input('Через пробел задайте меандр:\n')

meander, flag = functions.is_meander(mass, '')
n = len(meander)

if flag:
	size = int(input('Задайте размер клеток (обычно подходит 40):\n'))
	start = current_height // 2 - n // 2 * size
	print(start, start + n * size)

	C.create_rectangle(start, start, start + n * size, start + n * size, fill="white", outline="black")

	matrix = functions.meander_to_matrix(meander)
	for i in range(n):
		for j in range(n):
			pos_x = start + i * size
			pos_y = start + j * size
			if matrix[i][j] == 1:
				C.create_rectangle(pos_x, pos_y, pos_x + size, pos_y + size, fill="black")
			else:
				C.create_rectangle(pos_x, pos_y, pos_x + size, pos_y + size, fill="white", outline="black")

	C.pack()
	mainloop()
else:
	print('Вы ввели не меандр, попробуйте еще раз')
