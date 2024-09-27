import functions


count = int(input('Введите количество меандров, для которых вы хотите получить информацию:\n'))
m = input('Введите любой символ для вывода меандров, и нажмите Enter чтобы получить просто количество:\n')

for o in range(count):
    mass = input('Через пробел задайте меандр для проверки:\n')
    meander = list()

    for let in mass.split():
        if let.isdigit():
            meander.append(int(let))

    n = len(meander)
    mndrs = functions.Meanders(n)

    all_mndrs = mndrs.get_all_meanders(m)

    if meander in all_mndrs:
        functions.get_good_compositions(len(meander), meander)
    else:
        print('Вы ввели не меандр, попробуйте еще раз')
    print('')


# 5 8 7 6 9 2 3 4 1 10
