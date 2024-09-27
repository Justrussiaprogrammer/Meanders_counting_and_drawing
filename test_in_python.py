import functions


n = int(input('Задайте размер поиска меандров:\n'))
m = input('Введите любой символ для вывода меандров, и нажмите Enter чтобы получить просто количество:\n')

mndrs = functions.Meanders(n)
all_mndrs = mndrs.get_all_meanders(m)
mndrs.get_meanders_info()


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
