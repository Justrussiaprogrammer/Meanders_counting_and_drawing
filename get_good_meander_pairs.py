import functions


count = int(input('Введите количество меандров, для которых вы хотите получить информацию:\n'))
mode = input('Введите любой символ для вывода меандров, и нажмите Enter чтобы получить просто количество:\n')

for o in range(count):
    mass = input('Через пробел задайте меандр для проверки:\n')
    meander, flag = functions.is_meander(mass, mode)

    if flag:
        functions.get_good_compositions(meander)
    else:
        print('Вы ввели не меандр, попробуйте еще раз')
    print()
