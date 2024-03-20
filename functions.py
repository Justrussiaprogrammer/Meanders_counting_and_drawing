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


def print_screen(arr):
    for word in arr:
        print(word)


def do_screen(n):
    default = " " * (10 + n * 11)
    mass = [default] * (2 * n + 1)

    return mass


def find_max(start, finish, mass):
    answer = 0
    for i in range(start, finish + 1):
        answer = max(answer, mass[i])

    return answer


def do_combination(n, combination, mass):
    modified_combination = combination.copy()
    for i in range(len(combination)):
        modified_combination[i] -= 1

    line = [1] * (n + 1)
    lines = [line.copy(), line.copy()]
    for i in range(n):
        mass[n] = mass[n][:10 + i * 11] + str(i + 1) + mass[n][10 + i * 11 + 1:]

    last_pos = modified_combination[0]
    for i in range(1, n):
        start = min(last_pos, modified_combination[i])
        fin = max(last_pos, modified_combination[i])
        level = find_max(start, fin, lines[i % 2])
        for j in range(1, level + 1):
            position = n - ((-1) ** i) * j
            mass[position] = mass[position][:10 + start * 11] + "|" + mass[position][10 + start * 11 + 1:]
            mass[position] = mass[position][:10 + fin * 11] + "|" + mass[position][10 + fin * 11 + 1:]

        line_pos = n - ((-1) ** i) * level
        for j in range(10 + start * 11 + 1, 10 + fin * 11):
            if i % 2 == 1:
                mass[line_pos] = mass[line_pos][:j] + "_" + mass[line_pos][j + 1:]
            else:
                mass[line_pos] = mass[line_pos][:j] + "‾" + mass[line_pos][j + 1:]

        for j in range(start, fin + 1):
            lines[i % 2][j] += 1

        last_pos = modified_combination[i]

    return mass
