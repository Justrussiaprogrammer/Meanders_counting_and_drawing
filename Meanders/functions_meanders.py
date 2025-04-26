import os
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

        file_path = f'meanders_list/meanders{self.n}.txt'
        if os.path.exists(file_path):
            fd = open(file_path, 'r')
            info = fd.readlines()
            fd.close()
            for line in info:
                self.all_meanders.append([int(x) for x in line.split()])
        else:
            data, temp = os.pipe()
            os.write(temp, bytes(str(n) + "\n", "utf-8"))
            os.close(temp)
            subprocess.check_output(
                "../get_all_meanders", stdin=data, shell=True)

            fd = open(f"meanders.txt", 'r')
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
