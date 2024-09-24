import functions

count = int(input('Введите количество меандров, для которых вы хотите получить информацию:\n'))

for o in range(count):
    mass = input('Через пробел задайте меандр для проверки:\n')
    meander = list()

    for let in mass.split():
        if let.isdigit():
            meander.append(int(let))

    functions.GLOBAL_MATRICES = list()
    x_all = list()

    for i in range(9):
        x_all.append(set())

    functions.go_deep_to_build(8, 1, set([]), x_all, list())

    # for meand in functions.GLOBAL_MATRICES:
    #     print(meand)
    #     print('_' * 100)
    #     functions.get_good_compositions(len(meand), meand)

    functions.get_good_compositions(len(meander), meander)
    print()



# 5 8 7 6 9 2 3 4 1 10
