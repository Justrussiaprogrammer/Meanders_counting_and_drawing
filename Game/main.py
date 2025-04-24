import functions

import tkinter as tk
from tkinter import simpledialog, messagebox
import numpy as np
import os
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

if os.name == "posix":              # Для MacOs
    from tkmacosx import Button
    button_width = 80
    button_height = 30
elif os.name == "nt":               # Для Windows
    from tkinter import Button
    button_width = 10
    button_height = 3
else:
    print("Don't know the system")
    sys.exit(-1)


class MeanderApp:
    def __init__(self, root):
        self.root = root
        self.matrix = None
        self.current_frame = None
        self.meanders = None
        self.buttons = []
        self.__start_app()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def __start_app(self):
        self.clear_frame()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack()
        container = tk.Frame(self.current_frame)
        container.pack(expand=True, fill=tk.BOTH)

        size = simpledialog.askinteger("Размер меандра", "Введите размер меандра (целое число ≥ 2):",
                                       parent=self.root, minvalue=2)
        if not size:
            self.root.destroy()
            return

        self.size = size
        self.matrix = np.zeros((size, size), dtype=int)
        self.meanders = functions.Meanders(size).get_all_meanders()
        self.create_matrix_grid()

    def create_matrix_grid(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(expand=True, fill=tk.BOTH)

        container = tk.Frame(self.current_frame)
        container.pack(expand=True, fill=tk.BOTH)

        canvas = tk.Canvas(container)
        scrollbar_vertical = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar_horizontal = tk.Scrollbar(container, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar_horizontal.set, yscrollcommand=scrollbar_vertical.set)

        scrollbar_vertical.pack(side="right", fill="y")
        scrollbar_horizontal.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # Создание сетки кнопок
        self.buttons = [[] for _ in range(self.size)]
        for i in range(self.size):
            row_buttons = []
            for j in range(i + 1, self.size):
                btn = Button(
                    scrollable_frame,
                    width=button_width,
                    height=button_height,
                    bg=self.get_button_color(i, j),
                    command=lambda x=i, y=j: self.toggle_cell(x, y)
                )
                # else:
                #     btn = Button(
                #         row_frame,
                #         width=button_width,
                #         height=button_height,
                #         bg=self.get_button_color(i, j),
                #         command=lambda x=i, y=j: self.toggle_cell(x, y),
                #         state='disabled'
                #     )
                # if j == i + 1:
                #     btn.grid(row=i, column=0, padx=(2 + button_width) * i)
                # else:
                #     btn.grid(row=i, column=0, padx=)
                # btn.grid(row=i, column=0, padx=(2 + button_width) * i + j * button_width)
                column = j - 1  # Колонка внутри строки i
                # Отступ слева для первой кнопки в строке
                # padx_left = i * button_width if column == 0 else 2
                # print(padx_left)
                btn.grid(row=i, column=column, pady=2)
                self.buttons[i].append(btn)

        # Панель управления
        control_frame = tk.Frame(self.current_frame)
        control_frame.pack(pady=10)

        Button(control_frame, text="Сгенерировать", command=self.generate_meander).pack(side=tk.LEFT, padx=5)
        Button(control_frame, text="Завершить", command=self.exit).pack(side=tk.LEFT, padx=5)
        Button(control_frame, text="Инверсия матрицы", command=self.invert_matrix).pack(side=tk.LEFT, padx=5)
        canvas.update_idletasks()

    def invert_matrix(self):
        for i in range(self.size):
            for j in range(i + 1, self.size):
                self.toggle_cell(i, j)

    def exit(self):
        self.root.destroy()
        sys.exit(0)

    def toggle_cell(self, i, j):
        self.matrix[i][j] = 1 - self.matrix[i][j]
        self.update_button_color(i, j)

    def get_button_color(self, i, j):
        color = 'black' if self.matrix[i][j] == 1 else 'white'
        return color

    def update_button_color(self, i, j):
        # color = 'black' if self.matrix[i][j] == 1 else 'white'
        # self.buttons[i][j].config(bg=color)
        color = 'black' if self.matrix[i][j] == 1 else 'white'
        index = j - i - 1  # Индекс кнопки в списке self.buttons[i]
        self.buttons[i][index].config(bg=color)

    def generate_meander(self):
        meander = functions.matrix_to_meander(self.matrix)
        # print(meander)

        if not functions.check_meander(meander):
            messagebox.showerror("Ошибка", "Это не меандр!")
            return

        self.show_meander_plot(meander)

    def show_meander_plot(self, meander):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack()

        # Создание графика
        fig = functions.print_meanders(meander)

        canvas = FigureCanvasTkAgg(fig, master=self.current_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Кнопки управления
        control_frame = tk.Frame(self.current_frame)
        control_frame.pack(pady=10)

        Button(control_frame, text="Продолжить", command=self.create_matrix_grid).pack(side=tk.LEFT, padx=5)
        Button(control_frame, text="Начать сначала", command=self.__start_app).pack(side=tk.LEFT, padx=5)
        Button(control_frame, text="Завершить", command=self.exit).pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Генератор меандров")
    app = MeanderApp(root)
    root.mainloop()