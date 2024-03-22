import matplotlib.pyplot as plt
import numpy as np


def print_meanders(combination):
    cnt = -1
    plt.figure(figsize=(10, 8))
    plt.xticks(np.arange(1, len(combination) + 1, 1))
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim([-3, 3])
    ax.spines['bottom'].set_position(('data', 0))
    for i in range(len(combination) - 1):
        a = min(combination[i], combination[i + 1])
        b = max(combination[i], combination[i + 1])
        x = np.linspace(a, b, num=100, endpoint=True)
        plt.plot(x, ((((b - a)/2)**2 - (x - (a + b)/2)**2)**(1/2)) * cnt, color='g')
        cnt *= -1
    plt.show()



combination = [5, 6, 7, 4, 1, 2, 3, 8]
print_meanders(combination)
