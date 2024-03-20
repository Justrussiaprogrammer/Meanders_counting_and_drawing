import functions
import sys


print("Введите режим записи. Английская буква 'f' считается как файловый тип, иначе консоль:")
text = input()

if text.lower() == 'f':
    f = open('123.txt', 'w')
    sys.stdout = f

combination = [5, 4, 3, 2, 1, 6]
n = len(combination)


arr = functions.do_screen(n)
arr = functions.do_combination(n, combination, arr)
print('/' * 100)
functions.print_screen(arr)

if text.lower() == 'f':
    f.close()
