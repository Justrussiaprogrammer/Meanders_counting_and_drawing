import os
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time


class Meanders:
    def __init__(self, n):
        self.all_meanders = list()
        self.n = n

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("- Подождите, идет инициализация класса меандров -")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        start_time = time.time()

        data, temp = os.pipe()
        os.write(temp, bytes(str(n) + "\n", "utf-8"))
        os.close(temp)
        subprocess.check_output(
            "../get_all_meanders", stdin=data, shell=True)

        fd = open("../meanders.txt", 'r')
        info = fd.readlines()
        fd.close()
        for line in info:
            self.all_meanders.append([int(x) for x in line.split()])

        self.speed = time.time() - start_time
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("- Инициализация класса завершена -")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    def get_all_meanders(self):
        return self.all_meanders

    def get_meanders_info(self):
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

    def is_meander(self, digits):
        if digits in self.all_meanders:
            return True
        return False


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
