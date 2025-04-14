import functions


n = int(input('Задайте размер поиска меандров:\n'))
m = input('Введите любой символ для вывода меандров, и нажмите Enter чтобы получить просто количество:\n')

functions.Meanders(n).get_meanders_info()
