# JSON LOAD AND DUMP
# mass = list()
# for word in mass:
#     print(word)
#
# fd = open('info.json')
# data = json.load(fd)
# fd.close()
# data[str(x)] = mass
#
# fd = open('info.json', 'w')
# json.dump(data, fd, ensure_ascii=False, indent=2)
# fd.close()


# import functions
#
# functions.get_good_compositions(8, [3, 4, 5, 2, 1, 8, 7, 6])

import os

try:
    os.mkdir("meanders8")
except Exception:
    pass
finally:
    print('evr thing is ok')