import matplotlib.pyplot as plt
import numpy as np


def print_meanders(combination):
    cnt = -1
    plt.figure(figsize=(10, 10))
    plt.xticks(np.arange(1, len(combination) + 1, 1))
    for i in range(len(combination) - 1):
        a = min(combination[i], combination[i + 1])
        b = max(combination[i], combination[i + 1])
        x = np.linspace(a, b, num=100, endpoint=True)
        plt.plot(x, ((((b - a) / 2) ** 2 - (x - (a + b) / 2) ** 2) ** (1 / 2)) * cnt)
        cnt *= -1
    plt.show()


combination = [5, 4, 3, 2, 1, 6]
print_meanders(combination)
