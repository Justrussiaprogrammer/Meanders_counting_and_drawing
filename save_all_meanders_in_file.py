import matplotlib.pyplot as plt
import networkx as nx
import functions
import os


n = int(input('Задайте размер поиска меандров:\n'))
m = input('Введите любой символ для вывода меандров, и нажмите Enter чтобы получить просто количество:\n')
mndrs = functions.Meanders(n)
all_mndrs = mndrs.get_all_meanders(m)
mndrs.get_meanders_info()

try:
    os.mkdir("meanders" + str(n))
except Exception:
    pass

start_path = "meanders" + str(n) + "/number"
number = 1
for meander in all_mndrs:
    all_nodes = list()
    all_edges = list()
    d_pos = dict()
    G = nx.Graph()

    for i in range(len(meander)):
        G.add_node(i + 1)
        G.add_node(str(i + 1))
        G.add_edge(i + 1, str(meander[i]))
        d_pos[i + 1] = (2 * i, 2)
        d_pos[str(i + 1)] = (2 * i, 0)

    fig = plt.figure(figsize=(12, 12))
    nx.draw_networkx(G, pos=d_pos, with_labels=True, ax=fig.add_subplot())

    name = start_path + str(number) + ".png"
    number += 1
    fig.savefig(name)
