import os
import subprocess
import time
import numpy as np
import matplotlib.pyplot as plt


def print_meanders(combination):
    meander = [0] * len(combination)
    for i in range(len(combination)):
        meander[combination[i] - 1] = i + 1
    cnt = -1
    fig = plt.figure(figsize=(10, 8))
    plt.xticks(np.arange(1, len(combination) + 1, 1), labels=combination)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    for i in range(len(combination) - 1):
        a = min(meander[i], meander[i + 1])
        b = max(meander[i],meander[i + 1])
        x = np.linspace(a, b, num=100, endpoint=True)
        plt.plot(x, ((((b - a)/2)**2 - (x - (a + b)/2)**2)**(1/2)) * cnt, color='g')
        cnt *= -1
    plt.scatter(meander[0], 0, color='red', zorder=5, s=50)
    return fig


class Meanders:
    def __init__(self, n):
        self.all_meanders = list()
        self.n = n
        self.speed = 0

    def __init_list(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("- Подождите, идет инициализация класса меандров -")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        start_time = time.time()
        data, temp = os.pipe()
        os.write(temp, bytes(str(self.n) + "\n", "utf-8"))
        os.close(temp)
        subprocess.check_output(
            "get_all_meanders.exe", stdin=data, shell=True)

        fd = open(f"meanders.txt", 'r')
        info = fd.readlines()
        fd.close()
        for line in info:
            self.all_meanders.append([int(x) for x in line.split()])
            # print(self.all_meanders[-1])

        self.speed = time.time() - start_time
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("- Инициализация класса завершена -")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    def get_all_meanders(self):
        if len(self.all_meanders) == 0:
            self.__init_list()
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
        if len(self.all_meanders) == 0:
            n = len(digits)
            if n != self.n:
                return False
            visited = [False] * (n + 1)
            set_visited = set([])
            neighs = [0] * (n + 1)
            for digit in digits:
                if not visited[digit]:
                    for j in range(digit + 1, self.n + 1):
                        if visited[j] == 0:
                            neighs[digit] += 2 ** j
                            neighs[j] += 2 ** digit
                    if not check_noted(digit, set_visited, neighs):
                        return False
                    visited[digit] = True
                    set_visited.add(digit)
            return True
        else:
            if digits in self.all_meanders:
                return True
            return False


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


def meander_to_matrix(meander):
    n = len(meander)
    matrix = list()
    for i in range(n):
        matrix.append([0] * n)

    for i in range(n):
        for j in range(i + 1, n):
            if meander[i] > meander[j]:
                matrix[i][j] = 1
                matrix[j][i] = 1

    return matrix


# matrix = [[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1], [0, 0], [0]]
# meander = matrix_to_meander(matrix)
# print(meander)
