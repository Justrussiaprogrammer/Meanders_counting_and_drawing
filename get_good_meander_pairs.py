import functions

mass = input('Через пробел задайте меандр для проверки:\n')
meander = list()

for l in mass.split():
    if l.isdigit():
        meander.append(int(l))

functions.get_good_compositions(len(meander), meander)
