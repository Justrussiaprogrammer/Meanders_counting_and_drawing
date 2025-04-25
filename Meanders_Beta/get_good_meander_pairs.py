import Meanders_Beta.all_functions as mb_func

count = int(input('Введите количество меандров, для которых вы хотите получить информацию:\n'))
mode = input('Введите любой символ для вывода меандров, и нажмите Enter чтобы получить просто количество:\n')

for o in range(count):
    mass = input('Через пробел задайте меандр для проверки:\n')
    meander, flag = mb_func.is_meander(mass, mode)

    if flag:
        mb_func.get_good_compositions(meander)
    else:
        print('Вы ввели не меандр, попробуйте еще раз')
    print()
