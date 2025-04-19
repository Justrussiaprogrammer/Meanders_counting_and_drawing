import time
import numpy as np
import matplotlib.pyplot as plt


class Meanders:
    def __init__(self, n):
        self.all_meanders = list()
        self.n = n
        self.speed = 0

    def get_count_neighbours(self, pos, visited, neighs):
        answer = len(neighs[pos])
        for i in range(pos + 1, self.n + 1):
            if i not in visited:
                answer += 1

        return answer

    def __go_deep_to_build(self, is_even, visited, set_visited, neighs, to_answer, depth, mode=''):
        if depth == self.n:
            self.all_meanders.append(to_answer)
            if mode != '':
                print("Найдена комбинация номер {}:".format(len(self.all_meanders)), to_answer)
                print('-' * 100)
            return
        for i in range(is_even, self.n + 1, 2):
            if visited[i] == 0:
                for j in range(i + 1, self.n + 1):
                    if visited[j] == 0:
                        neighs[i] += 2 ** j
                        neighs[j] += 2 ** i
                if not check_noted(i, set_visited, neighs):
                    for j in range(i + 1, self.n + 1):
                        if visited[j] == 0:
                            neighs[i] -= 2 ** j
                            neighs[j] -= 2 ** i
                    continue
                visited[i] = 1
                set_visited.add(i)
                self.__go_deep_to_build(3 - is_even, visited, set_visited, neighs, to_answer + [i], depth + 1, mode=mode)
                for j in range(i + 1, self.n + 1):
                    if visited[j] == 0:
                        neighs[i] -= 2 ** j
                        neighs[j] -= 2 ** i
                visited[i] = 0
                set_visited.remove(i)

    def get_all_meanders(self, mode=''):
        if len(self.all_meanders) < 1:
            start_time = time.time()
            self.__go_deep_to_build(1, [0] * (self.n + 1), set([]), [0] * (self.n + 1), list(), 0, mode=mode)
            self.speed = time.time() - start_time

        return self.all_meanders

    def get_meanders_info(self, mode=''):
        if len(self.all_meanders) < 1:
            start_time = time.time()
            self.__go_deep_to_build(1, [0] * (self.n + 1), set([]), [0] * (self.n + 1), list(), 0, mode=mode)
            self.speed = time.time() - start_time

        answer = len(self.all_meanders)
        string_for_meanders1 = "найден"
        string_for_meanders2 = "меандр"
        if answer % 10 > 4 or (4 < answer % 100 < 21):
            string_for_meanders1 = "найдено"
            string_for_meanders2 = "меандров"
        elif answer % 10 > 1:
            string_for_meanders1 = "найдено"
            string_for_meanders2 = "меандра"
        print("Для числа", self.n, string_for_meanders1, answer, string_for_meanders2)
        print("Всего прошло:", self.speed)


def check_noted(pos, visited, neighs):
    for x in visited:
        if (2 ** x) & neighs[pos] == 2 ** x:
            union = neighs[pos] & neighs[x]
            if union.bit_count() % 2 == 1:
                return False
        else:
            union = neighs[pos] & neighs[x]
            if union.bit_count() % 2 == 0:
                return False
    return True


def find_max(start, finish, mass):
    answer = 0
    for i in range(start, finish + 1):
        answer = max(answer, mass[i])

    return answer


def do_combination(n, combination):
    default = " " * (10 + n * 11)
    mass = [default] * (2 * n + 1)
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
            if meander[i] > meander[j]:
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


def addition_in_z2(A, B):
    """
    :param A: list[list]; задаёт матрицу-множитель 1
    :param B: list[list]; задаёт матрицу-множитель 2
    """
    n = len(A)
    m = len(B)
    if n != m:
        print("bad sizes")
        return list()
    local_arr = list()
    for j in range(n):
        local_arr.append([0] * n)

    for i in range(n):
        for j in range(n):
            local_arr[i][j] = (A[i][j] + B[i][j]) % 2

    return local_arr


def matrix_to_meander(matrix):
    """
    :param matrix: list[list]; задаёт матрицу меандра
    """
    n = len(matrix)
    ans_meander = [0] * n
    cur_min_free = 1
    used = [False] * n
    for i in range(n):
        line_sum = sum(matrix[i][i:])

        pos = cur_min_free
        plus = 0
        while plus != line_sum:
            if not used[pos - 1]:
                plus += 1
            pos += 1
        while used[pos - 1]:
            pos += 1

        ans_meander[i] = pos
        used[pos - 1] = True
        if pos == cur_min_free:
            cur_min_free += 1

    return ans_meander


def get_good_compositions(meander):
    """
    :param meander: list; задаёт меандр
    """
    n = len(meander)
    zero = [x + 1 for x in range(n)]
    count_of_pairs = 0

    all_meanders = Meanders(n).get_all_meanders()

    matrices_mass = list()
    for word in all_meanders:
        matrices_mass.append(meander_to_matrix(word))

    local_matrix = meander_to_matrix(meander)
    print('Данный меандр (Первый множитель):')
    print(meander)
    print('Подходящие варианты:')
    for local_meander in all_meanders:
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
                        print(matrix_to_meander(addition_in_z2(meander_to_matrix(meander), A)))
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
                    print('')
                    count_of_pairs += 1

def is_meander(letters, out):
    meander = list()

    for let in letters.split():
        if let.isdigit():
            meander.append(int(let))

    all_meanders = Meanders(len(meander)).get_all_meanders(mode=out)

    if meander not in all_meanders:
        return [], False
    return meander, True


def print_meanders(combination):
    cnt = -1
    fig = plt.figure(figsize=(10, 8))
    plt.xticks(np.arange(1, len(combination) + 1, 1))
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    for i in range(len(combination) - 1):
        a = min(combination[i], combination[i + 1])
        b = max(combination[i], combination[i + 1])
        x = np.linspace(a, b, num=100, endpoint=True)
        plt.plot(x, ((((b - a)/2)**2 - (x - (a + b)/2)**2)**(1/2)) * cnt, color='g')
        cnt *= -1
    return fig
