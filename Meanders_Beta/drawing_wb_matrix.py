import Meanders_Beta.all_functions as all_func

mass = input('Через пробел задайте меандр:\n')

meander, flag = all_func.is_meander(mass, '')
n = len(meander)

if flag:
	size = int(input('Задайте размер клеток (обычно подходит 40):\n'))
	flag_save = len(input('Нужно ли сохранять в файл? Напишите любой символ если да, иначе нажмите Enter:\n')) > 0

	all_func.get_wb_matrix(meander, size=size, out_file=flag_save)

	print("Задача выполнена")
else:
	print('Вы ввели не меандр, попробуйте еще раз')
