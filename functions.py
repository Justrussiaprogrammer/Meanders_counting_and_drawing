import numpy as np


GLOBAL_MATRICES = list()


def get_count_neighbours(n, pos, visited, neighs):
    answer = len(neighs[pos])
    for i in range(pos + 1, n + 1):
        if i not in visited:
            answer += 1

    return answer


def check_noted(pos, visited, neighs):
    for x in visited:
        if x in neighs[pos]:
            union = neighs[pos] | neighs[x]
            if len(union) % 2 != 0:
                return False
        else:
            union = neighs[pos] | neighs[x]
            if len(union) % 2 != 1:
                return False
    return True


def go_deep_to_build(n, is_even, visited, neighs, to_answer, mode=''):
    global GLOBAL_MATRICES
    if len(visited) == n:
        GLOBAL_MATRICES.append(to_answer)
        if mode != '':
            print("Найдена комбинация номер {}:".format(len(GLOBAL_MATRICES)), to_answer)
            print('-' * 100)
        return
    for i in range(is_even, n + 1, 2):
        if i not in visited:
            for j in range(i + 1, n + 1):
                if j not in visited:
                    neighs[i].add(j)
                    neighs[j].add(i)
            if not check_noted(i, visited, neighs):
                for j in range(i + 1, n + 1):
                    if j not in visited:
                        neighs[i].remove(j)
                        neighs[j].remove(i)
                continue
            visited.add(i)
            go_deep_to_build(n, 3 - is_even, visited, neighs, to_answer + [i], mode=mode)
            for j in range(i + 1, n + 1):
                if j not in visited:
                    neighs[i].remove(j)
                    neighs[j].remove(i)
            visited.remove(i)


def print_screen(arr):
    for word in arr:
        print(word)


def do_screen(n):
    default = " " * (10 + n * 11)
    mass = [default] * (2 * n + 1)

    return mass


def find_max(start, finish, mass):
    answer = 0
    for i in range(start, finish + 1):
        answer = max(answer, mass[i])

    return answer


def do_combination(n, combination, mass):
    modified_combination = combination.copy()
    for i in range(len(combination)):
        modified_combination[i] -= 1

    line = [1] * (n + 1)
    lines = [line.copy(), line.copy()]
    for i in range(n):
        mass[n] = mass[n][:10 + i * 11] + str(i + 1) + mass[n][10 + i * 11 + 1:]

    last_pos = modified_combination[0]
    for i in range(1, n):
        start = min(last_pos, modified_combination[i])
        fin = max(last_pos, modified_combination[i])
        level = find_max(start, fin, lines[i % 2])
        for j in range(1, level + 1):
            position = n - ((-1) ** i) * j
            mass[position] = mass[position][:10 + start * 11] + "|" + mass[position][10 + start * 11 + 1:]
            mass[position] = mass[position][:10 + fin * 11] + "|" + mass[position][10 + fin * 11 + 1:]

        line_pos = n - ((-1) ** i) * level
        for j in range(10 + start * 11 + 1, 10 + fin * 11):
            if i % 2 == 1:
                mass[line_pos] = mass[line_pos][:j] + "_" + mass[line_pos][j + 1:]
            else:
                mass[line_pos] = mass[line_pos][:j] + "‾" + mass[line_pos][j + 1:]

        for j in range(start, fin + 1):
            lines[i % 2][j] += 1

        last_pos = modified_combination[i]

    return mass


def meander_to_matrix(meander):
    n = len(meander)
    matrix = list()
    for i in range(n):
        matrix.append([0] * n)

    meander_string = ''.join([str(x) for x in meander])
    for i in range(n):
        for j in range(i + 1, n):
            if meander_string.find(str(i + 1)) > meander_string.find(str(j + 1)):
                matrix[i][j] = 1
                matrix[j][i] = 1
    return matrix


def mask_to_matrix(n, mask):
    local_arr = list()
    for j in range(n):
        local_arr.append([0] * n)

    step = 2 ** (n * (n - 1) // 2 - 1)
    i = 0
    j = 1
    while step > 0:
        if step <= mask:
            mask -= step
            local_arr[i][j] = 1
            local_arr[j][i] = 1
        j += 1
        if j == n:
            i += 1
            j = i + 1
        step /= 2

    return local_arr


def composition_in_z2(n, A, B):
    local_arr = list()
    for j in range(n):
        local_arr.append([0] * n)

    for i in range(n):
        for j in range(n):
            local = 0
            for o in range(n):
                local += A[i][o] * B[o][j]
            local_arr[i][j] = local % 2

    return local_arr


def addition_in_z2(n, A, B):
    local_arr = list()
    for j in range(n):
        local_arr.append([0] * n)

    for i in range(n):
        for j in range(n):
            local_arr[i][j] = (A[i][j] + B[i][j]) % 2

    return local_arr


def matrix_to_meander(matrix):
    n = len(matrix)
    ans_meander = [i for i in range(1, n + 1)]
    cur_numbers = [i for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] == 1:
                x = ans_meander[cur_numbers[i]]
                ans_meander[cur_numbers[i]] = ans_meander[cur_numbers[j]]
                ans_meander[cur_numbers[j]] = x
                y = cur_numbers[i]
                cur_numbers[i] = cur_numbers[j]
                cur_numbers[j] = y
    return ans_meander


def get_good_compositions(n, meander):
    global GLOBAL_MATRICES
    GLOBAL_MATRICES = list()
    x_all = list()
    zero = [x + 1 for x in range(n)]
    count_of_pairs = 0

    for i in range(n + 1):
        x_all.append(set())

    go_deep_to_build(n, 1, set([]), x_all, list())

    matrices_mass = list()
    for word in GLOBAL_MATRICES:
        matrices_mass.append(meander_to_matrix(word))

    local_matrix = meander_to_matrix(meander)
    print('Данный меандр (Первый множитель):')
    print(meander)
    print('Подходящие варианты:')
    for local_meander in GLOBAL_MATRICES:
        A = meander_to_matrix(local_meander)
        if A != local_matrix:
            C = composition_in_z2(n, local_matrix, A)
            D = composition_in_z2(n, A, local_matrix)
            if C == D:
                if C != A and C != local_matrix:
                    if matrix_to_meander(C) == zero:
                        print(f'Подходящая пара номер {count_of_pairs} (получился ноль, выводится сумма):')
                        print('>' * 100)
                        print('Второе слагаемое:')
                        print(local_meander)
                        print('-' * 100)
                        print('Сумма:')
                        print(matrix_to_meander(addition_in_z2(n, meander_to_matrix(meander), A)))
                        print('<' * 100)
                    else:
                        print(f'Подходящая пара номер {count_of_pairs} (выводится произведение):')
                        print('>' * 100)
                        print('Второй множитель:')
                        print(local_meander)
                        print('-' * 100)
                        print('Произведение:')
                        print(matrix_to_meander(C))
                        print('<' * 100)
                    print()
                    count_of_pairs += 1
    print('end')
    GLOBAL_MATRICES = list()


# a = meander_to_matrix([1, 4, 3, 2, 5, 6])
# b = meander_to_matrix([1, 6, 5, 4, 3, 2])
# c = composition_in_z2(6, a, b)
#
# print(np.array(c))
