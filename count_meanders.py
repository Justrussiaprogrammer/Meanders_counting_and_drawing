import functions


n = int(input('Задайте размер поиска меандров:\n'))
m = input('Введите любой символ для вывода меандров, и нажмите Enter чтобы получить просто количество:\n')

mndrs = functions.Meanders(n)
all_mndrs = mndrs.get_all_meanders(m)
mndrs.get_meanders_info()
