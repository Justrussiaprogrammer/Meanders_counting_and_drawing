import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Canvas
from PIL import Image, ImageDraw
import Meanders.functions_meanders as func_meanders


def get_wb_matrix(meander, current_height=800, current_width=800, size=40, filename="drawing_wb_matrix.png",
                  out_file=True):
    image = None
    draw = None
    root = None
    my_canvas = None
    n = len(meander)
    if out_file:
        image = Image.new("RGB", (current_height, current_height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
    else:
        root = Tk()
        my_canvas = Canvas(root, bg="white", height=current_height, width=current_width)
        my_canvas.pack()

    start = current_height // 2 - n // 2 * size
    matrix = func_meanders.meander_to_matrix(meander)
    colors = {0: "white", 1: "black"}
    for i in range(n):
        for j in range(i):
            pos_x = start + i * size
            pos_y = start + j * size
            if out_file:
                draw.rectangle((pos_x, pos_y, pos_x + size, pos_y + size), fill=colors[matrix[i][j] % 2],
                               outline=colors[1 - matrix[i][j] % 2])
            else:
                my_canvas.create_rectangle(pos_x, pos_y, pos_x + size, pos_y + size, fill=colors[matrix[i][j] % 2],
                                           outline=colors[1 - matrix[i][j] % 2])

    if out_file:
        image.save(filename)
    else:
        root.mainloop()


def print_meanders(combination):
    cnt = -1
    fig = plt.figure(figsize=(10, 8))
    plt.xticks(np.arange(1, len(combination) + 1, 1))
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    for i in range(len(combination) - 1):
        a = min(combination[i], combination[i + 1])
        b = max(combination[i], combination[i + 1])
        x = np.linspace(a, b, num=100, endpoint=True)
        plt.plot(x, ((((b - a)/2)**2 - (x - (a + b)/2)**2)**(1/2)) * cnt, color='g')
        cnt *= -1
    return fig
