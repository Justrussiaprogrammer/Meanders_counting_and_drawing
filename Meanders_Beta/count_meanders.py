import Meanders_Beta.all_functions as mb_func

n = int(input('Задайте размер поиска меандров:\n'))
m = input('Введите любой символ для вывода меандров, и нажмите Enter чтобы получить просто количество:\n')

mb_func.Meanders(n).get_meanders_info()
