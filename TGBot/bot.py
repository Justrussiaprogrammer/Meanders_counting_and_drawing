
import functions
import drawing2

import tkinter as tk
from tkinter import simpledialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MeanderApp:
    def __init__(self, root):
        self.root = root
        self.matrix = None
        self.current_frame = None
        self.buttons = []
        self.start_app()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def start_app(self):
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
        self.create_matrix_grid()

    def create_matrix_grid(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack()

        container = tk.Frame(self.current_frame)
        container.pack(expand=True, fill=tk.BOTH)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

        # Создание сетки кнопок
        self.buttons = []
        for i in range(self.size):
            row_frame = tk.Frame(self.current_frame)
            row_frame.pack()
            row_buttons = []
            for j in range(self.size):
                btn = tk.Button(
                    row_frame,
                    width=3,
                    height=1,
                    bg='white',
                    command=lambda x=i, y=j: self.toggle_cell(x, y)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Панель управления
        control_frame = tk.Frame(self.current_frame)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Сгенерировать", command=self.generate_meander).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Завершить", command=self.root.destroy).pack(side=tk.LEFT, padx=5)

    def toggle_cell(self, i, j):
        self.matrix[i][j] = 1 - self.matrix[i][j]
        self.update_button_color(i, j)

    def check_meander(self, meander, out):
        n = len(meander)
        mndrs = functions.Meanders(n)
        all_mndrs = mndrs.get_all_meanders(mode=out)
        if meander not in all_mndrs:
            return False
        return True

    def update_button_color(self, i, j):
        color = 'black' if self.matrix[i][j] == 1 else 'white'
        self.buttons[i][j].config(bg=color)

    def generate_meander(self):
        meander = functions.matrix_to_meander(self.matrix)

        if not self.check_meander(meander, ''):
            messagebox.showerror("Ошибка", "Это не меандр!")
            return

        self.show_meander_plot(meander)

    def show_meander_plot(self, meander):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack()

        # Создание графика
        fig = drawing2.print_meanders(meander)

        canvas = FigureCanvasTkAgg(fig, master=self.current_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Кнопки управления
        control_frame = tk.Frame(self.current_frame)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Продолжить", command=self.start_app).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Завершить", command=self.root.destroy).pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Генератор меандров")
    app = MeanderApp(root)
    root.mainloop()