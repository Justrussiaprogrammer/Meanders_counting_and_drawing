import time
import matplotlib.pyplot as plt
import networkx as nx


def get_count_neighbours(n, pos, visited, neighs):
    answer = len(neighs[pos])
    for i in range(pos + 1, n + 1):
        if i not in visited:
            answer += 1

    return answer


def check_noted(n, pos, visited, neighs):
    for x in visited:
        if x in neighs[pos]:
            union = neighs[pos] | neighs[x]
            if len(union) % 2 != 0:
                return False
        else:
            union = neighs[pos] | neighs[x]
            if len(union) % 2 != 1:
                return False
    return True


def go_deep_to_build(n, is_even, visited, neighs, to_answer):
    global global_answer
    if len(visited) == n:
        all_meanders.append(to_answer)
        global_answer += 1
        print("Найдена комбинация номер {}:".format(global_answer), to_answer)
        print('-' * 100)
        return
    for i in range(is_even, n + 1, 2):
        if i not in visited:
            for j in range(i + 1, n + 1):
                if j not in visited:
                    neighs[i].add(j)
                    neighs[j].add(i)
            if not check_noted(n, i, visited, neighs):
                for j in range(i + 1, n + 1):
                    if j not in visited:
                        neighs[i].remove(j)
                        neighs[j].remove(i)
                continue
            visited.add(i)
            go_deep_to_build(n, 3 - is_even, visited, neighs, to_answer + [i])
            for j in range(i + 1, n + 1):
                if j not in visited:
                    neighs[i].remove(j)
                    neighs[j].remove(i)
            visited.remove(i)


all_meanders = list()
start_time = time.time()
global_answer = 0
print('Задайте размер поиска меандров:')
x = int(input())
X_all = list()

for i in range(x + 1):
    X_all.append(set())

go_deep_to_build(x,1, set([]), X_all, list())
string_for_meanders1 = "найден"
string_for_meanders2 = "меандр"
if global_answer % 10 > 4 or (4 < global_answer % 100 < 21):
    string_for_meanders1 = "найдено"
    string_for_meanders2 = "меандров"
elif global_answer % 10 > 1:
    string_for_meanders1 = "найдено"
    string_for_meanders2 = "меандра"
print("Для числа", x, string_for_meanders1, global_answer, string_for_meanders2)
print("Всего прошло:", time.time() - start_time)

number = 1
for meander in all_meanders:
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
    name = 'meanders8/number' + str(number) + ".png"
    number += 1
    fig.savefig(name)
