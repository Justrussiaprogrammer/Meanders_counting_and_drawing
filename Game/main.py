import functions_copy as functions

import tkinter as tk
from tkinter import simpledialog, messagebox
import numpy as np
import os
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt

COLORS = {
    "bg": "#7FFF00",       # Основной фон (тёмно-серо-синий)
    "fg": "#000000",       # Цвет текста (светло-серый)
    "widget_bg": "#3B4252",# Фон виджетов (серо-синий)
    "active_bg": "#434C5E",# Активный фон кнопок
    "highlight": "#81A1C1",# Акцентный цвет (синий)
    "error": "#BF616A"     # Цвет ошибок (красный)
}

FONTS = {
        "default": ("Arial", 10),
        "title": ("Arial", 12, "bold"),
        "dialog_large": ("Arial", 16),  # Крупный шрифт для текста
        "dialog_input": ("Arial", 14),  # Шрифт для полей ввода
        "dialog_button": ("Arial", 12, "bold")  # Шрифт для кнопок
    }

if os.name == "posix":              # Для MacOs
    from tkmacosx import Button
    button_width = 100
    button_height = 50
    button_args = {
        "activebackground": COLORS["active_bg"],
        "borderless": True,
        "highlightthickness": 0
    }
elif os.name == "nt":               # Для Windows
    from tkinter import Button
    button_width = 10
    button_height = 3
    button_args = {
        "activebackground": COLORS["active_bg"],
        "relief": "flat"
    }
else:
    print("Don't know the system")
    sys.exit(-1)


class MeanderApp:
    def __init__(self, root):
        self.current_fig = None
        self.root = root
        self.root.configure(bg=COLORS["bg"])
        self.matrix = None
        self.current_frame = None
        self.meanders = None
        self.buttons = []
        self.size = 2
        self.error_label = None
        self.plot_window = None  # Добавляем ссылку на окно графика
        self.plot_canvas = None  # Добавляем ссылку на холст
        self.__start_app()
        self.create_error_label()

    def create_error_label(self):
        self.error_label = tk.Label(
            self.root,
            text="",
            font=FONTS["dialog_large"],
            bg=COLORS["bg"],
            fg=COLORS["error"]
        )
        self.error_label.pack(pady=5, fill=tk.X)

    def show_error(self, message):
        self.error_label.config(text=message)
        self.root.after(5000, lambda: self.error_label.config(text=""))

    def output_meander(self):
        meander = functions.matrix_to_meander(self.matrix)

        if not self.meanders.is_meander(meander):
            self.show_error("Ошибка: Это не меандр!")
            return

        output_window = tk.Toplevel(self.root)
        output_window.title("Меандрическая последовательность")
        output_window.geometry("600x200")

        meander_text = ", ".join(map(str, meander))
        label = tk.Label(
            output_window,
            text=meander_text,
            font=FONTS["dialog_large"],
            padx=20,
            pady=20
        )
        label.pack(expand=True)

        Button(
            output_window,
            text="Закрыть",
            command=output_window.destroy,
            **button_args
        ).pack(pady=10)

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    # Модифицируем метод __start_app и continue_after_mode
    def __start_app(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack()
        size_dialog = tk.Toplevel(self.root)
        size_dialog.title("Размер меандра")
        size_dialog.geometry("800x300")  # Увеличиваем размер

        tk.Label(
            size_dialog,
            text="Введите размер меандра (целое число ≥ 2):",
            font=FONTS["dialog_large"]
        ).pack(pady=20)

        size_var = tk.IntVar()
        entry = tk.Entry(
            size_dialog,
            textvariable=size_var,
            font=FONTS["dialog_input"],
            width=15
        )
        entry.pack(pady=20)

        def on_ok():
            self.size = size_var.get()
            size_dialog.destroy()
            if self.size >= 2:
                self.matrix = np.zeros((self.size, self.size), dtype=int)
                self.meanders = functions.Meanders(self.size)
                self.create_matrix_grid()
            else:
                messagebox.showerror("Ошибка", "Размер должен быть ≥ 2!")
                self.root.destroy()

        tk.Button(
            size_dialog,
            text="OK",
            command=on_ok,
            font=FONTS["dialog_button"],
            width=10,
            height=2
        ).pack(pady=20)

        size_dialog.transient(self.root)
        size_dialog.grab_set()
        self.root.wait_window(size_dialog)

    def meander_mode(self):
        meander_dialog = tk.Toplevel(self.root)
        meander_dialog.title("Ввод меандра")
        meander_dialog.geometry("800x300")  # Увеличиваем размер

        tk.Label(
            meander_dialog,
            text="Через запятую введите меандр:",
            font=FONTS["dialog_large"]
        ).pack(pady=20)

        meander_var = tk.StringVar()
        entry = tk.Entry(
            meander_dialog,
            textvariable=meander_var,
            font=FONTS["dialog_input"],
            width=15
        )
        entry.pack(pady=20)

        def on_ok():
            inp = meander_var.get()
            meander_dialog.destroy()
            if self.size >= 2:
                self.matrix = np.zeros((self.size, self.size), dtype=int)
                meander = [int(num.strip()) for num in inp.split(',')]

                if not self.meanders.is_meander(meander):
                    self.show_error("Ошибка: Это не меандр!")
                    return

                # self.show_meander_plot(meander)
                self.matrix = functions.meander_to_matrix(meander)
                self.create_matrix_grid()

            else:
                messagebox.showerror("Ошибка", "Размер должен быть ≥ 2!")
                self.root.destroy()
        tk.Button(
            meander_dialog,
            text="OK",
            command=on_ok,
            font=FONTS["dialog_button"],
            width=10,
            height=2
        ).pack(pady=20)
        meander_dialog.transient(self.root)
        meander_dialog.grab_set()
        self.root.wait_window(meander_dialog)

    def create_matrix_grid(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=COLORS["bg"])
        self.current_frame.pack(expand=True, fill=tk.BOTH)

        container = tk.Frame(self.current_frame, bg=COLORS["bg"])
        container.pack(expand=True, fill=tk.BOTH)

        canvas = tk.Canvas(container, bg=COLORS["bg"], highlightthickness=0)
        scrollbar_vertical = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar_horizontal = tk.Scrollbar(container, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar_args = {
            "bg": COLORS["widget_bg"],
            "activebackground": COLORS["active_bg"],
            "troughcolor": COLORS["bg"],
            "relief": "flat"
        }
        scrollbar_vertical.configure(**scrollbar_args)
        scrollbar_horizontal.configure(**scrollbar_args)

        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg"])

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
            for j in range(i + 1, self.size):
                btn = Button(
                    scrollable_frame,
                    width=button_width,
                    height=button_height,
                    bg=self.get_button_color(i, j),
                    command=lambda x=i, y=j: self.toggle_cell(x, y),
                    **button_args,
                    fg=COLORS["fg"],
                    font=FONTS["default"],
                )
                column = j - 1
                btn.grid(row=i, column=column, padx=5, pady=2)
                self.buttons[i].append(btn)

        # Панель управления
        control_frame = tk.Frame(self.current_frame, bg=COLORS["bg"])
        control_frame.pack(pady=10)

        control_buttons = [
            ("Начать сначала", self.__start_app),
            ("Сгенерировать", self.generate_meander),
            ("Инверсия матрицы", self.invert_matrix),
            ("Ввести меандр", self.meander_mode),
            ("Вывести меандр", self.output_meander),
            ("Завершить", self.exit)
        ]

        for text, cmd in control_buttons:
            Button(control_frame,
                   text=text,
                   command=cmd,
                   **button_args,
                   fg=COLORS["fg"],
                   font=FONTS["dialog_large"],
                   width=20,
                   height=3,
                   activeforeground=COLORS["fg"]
                   ).pack(side=tk.LEFT, padx=5)
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

        # if not self.meanders.is_meander(meander):
        #     # self.show_error("Ошибка: Это не меандр!")
        #     # return

        self.show_meander_plot(meander)

    def show_meander_plot(self, meander):
        plt.style.use('dark_background' if COLORS["bg"] == "#7FFF00" else 'classic')

        # Если окно существует, очищаем содержимое
        if self.plot_window and tk.Toplevel.winfo_exists(self.plot_window):
            # Уничтожаем все виджеты в окне
            for widget in self.plot_window.winfo_children():
                widget.destroy()
        else:
            # Создаем новое окно, если его нет
            self.plot_window = tk.Toplevel(self.root)
            self.plot_window.title("График меандра")
            self.plot_window.geometry("800x600")
            self.plot_window.protocol("WM_DELETE_WINDOW", self.close_plot_window)

        # Создаем основной контейнер
        container = tk.Frame(self.plot_window, bg=COLORS["bg"])
        container.pack(expand=True, fill=tk.BOTH)

        # Создаем и размещаем график
        self.current_fig = functions.print_meanders(meander)
        self.plot_canvas = FigureCanvasTkAgg(self.current_fig, master=container)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().configure(bg=COLORS["bg"])
        self.plot_canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        # Создаем новый фрейм для кнопок
        control_frame = tk.Frame(container, bg=COLORS["bg"])
        control_frame.pack(pady=10)

        # Добавляем кнопку закрытия
        Button(
            control_frame,
            text="Закрыть график",
            command=self.close_plot_window,
            **button_args,
            fg=COLORS["fg"],
            width=20,
            height=3,
            font=FONTS["dialog_large"],
            activeforeground=COLORS["fg"]
        ).pack(side=tk.LEFT, padx=5)

    def close_plot_window(self):
        if self.plot_window:
            # Закрываем фигуру matplotlib
            plt.close(self.current_fig)
            # Уничтожаем окно
            self.plot_window.destroy()
            self.plot_window = None


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Генератор меандров")
    app = MeanderApp(root)
    root.mainloop()
