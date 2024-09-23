import time
import functions


n = int(input('Задайте размер поиска меандров:\n'))
X_all = list()
m = input('Введите любой символ для вывода меандров, и нажмите Enter чтобы получить просто количество:\n')

start_time = time.time()
for i in range(n + 1):
    X_all.append(set())

functions.go_deep_to_build(n, 1, set([]), X_all, list(), mode=m)
string_for_meanders1 = "найден"
string_for_meanders2 = "меандр"
global_answer = len(functions.GLOBAL_MATRICES)
if global_answer % 10 > 4 or (4 < global_answer % 100 < 21):
    string_for_meanders1 = "найдено"
    string_for_meanders2 = "меандров"
elif global_answer % 10 > 1:
    string_for_meanders1 = "найдено"
    string_for_meanders2 = "меандра"
print("Для числа", n, string_for_meanders1, global_answer, string_for_meanders2)
print("Всего прошло:", time.time() - start_time)


# fd = open('info.json')
# data = json.load(fd)
# fd.close()
#
# matrixes = data[str(x)]
#
# for i in range(len(matrixes)):
#     local_matrix = matrixes[i]
#     print(np.array(local_matrix))
#     print('Подходящие варианты:')
#     for j in range(i + 1, len(matrixes)):
#         A = matrixes[j]
#         C = functions.composition_in_z2(x, local_matrix, A)
#         D = functions.composition_in_z2(x, A, local_matrix)
#         if C == D:
#             print(np.array(A))
#             print('>' * 100)
#             print(np.array(C))
#             print('-' * 100)
#     print('end')
