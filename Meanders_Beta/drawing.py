import Meanders_Beta.all_functions as mb_func
import sys


meander = list(map(int, input("Введите меандр для рисования через пробел:\n").split()))
n = len(meander)
input_type = input("Введите режим записи: буква <f> означает запись в файл, любой иной вариант выводится в консоль:\n")

arr = mb_func.do_combination(n, meander)

if input_type == 'f':
    f = open('drawing.txt', 'w')
    sys.stdout = f

print('/' * 100)
for line in arr:
    if len(line) != line.count(' '):
        print(line)
print('/' * 100)

if input_type == 'f':
    f.close()
