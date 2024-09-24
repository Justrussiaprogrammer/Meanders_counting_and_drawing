import functions

count = int(input('Введите количество меандров, для которых вы хотите получить информацию:\n'))

for o in range(count):
    mass = input('Через пробел задайте меандр для проверки:\n')
    meander = list()

    for let in mass.split():
        if let.isdigit():
            meander.append(int(let))

    n = len(meander)
    functions.GLOBAL_MATRICES = list()
    x_all = list()

    for i in range(n + 1):
        x_all.append(set())

    functions.go_deep_to_build(n, 1, set([]), x_all, list())

    if meander in functions.GLOBAL_MATRICES:
        functions.get_good_compositions(len(meander), meander)
    else:
        print('Вы ввели не меандр, попробуйте еще раз')
    print()



# 5 8 7 6 9 2 3 4 1 10
