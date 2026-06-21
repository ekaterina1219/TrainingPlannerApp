import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

DATA_FILE = "trainings.json"

class TrainingPlannerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Планировщик тренировок")
        self.root.geometry("650x500")

        # Загрузка сохраненных данных при старте
        self.trainings = self.load_data()

        # --- БЛОК ВВОДА ДАННЫХ ---
        frame_input = tk.LabelFrame(root, text=" Добавление тренировки ", padding=10)
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Дата:").grid(row=0, column=0, sticky="w")
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.insert(0, "2026-06-21")  # Дефолтное значение даты
        self.entry_date.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_input, text="Тип:").grid(row=0, column=2, sticky="w")
        self.entry_type = tk.Entry(frame_input)
        self.entry_type.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(frame_input, text="Длительность:").grid(
            row=0, column=4, sticky="w"
        )
        self.entry_duration = tk.Entry(frame_input, width=10)
        self.entry_duration.grid(row=0, column=5, padx=5, pady=2)

        btn_add = tk.Button(
            frame_input, text="Добавить", command=self.add_training, bg="#4CAF50", fg="white"
        )
        btn_add.grid(row=0, column=6, padx=10)

        # --- БЛОК ФИЛЬТРОВ ---
        frame_filters = tk.LabelFrame(root, text=" Фильтры поиска ", padding=10)
        frame_filters.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filters, text="Фильтр по типу:").grid(
            row=0, column=0, sticky="w"
        )
        self.filter_type = tk.Entry(frame_filters)
        self.filter_type.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_filters, text="Фильтр по дате:").grid(
            row=0, column=2, sticky="w"
        )
        self.filter_date = tk.Entry(frame_filters)
        self.filter_date.grid(row=0, column=3, padx=5, pady=2)

        btn_apply = tk.Button(
            frame_filters, text="Применить", command=self.update_table
        )
        btn_apply.grid(row=0, column=4, padx=5)

        btn_clear = tk.Button(
            frame_filters, text="Сбросить", command=self.clear_filters
        )
        btn_clear.grid(row=0, column=5, padx=5)

        # --- ТАБЛИЦА ВЫВОДА ---
        self.tree = ttk.Treeview(
            root, columns=("Date", "Type", "Duration"), show="headings"
        )
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Type", text="Тип тренировки")
        self.tree.heading("Duration", text="Длительность (мин)")

        # Настройка ширины колонок
        self.tree.column("Date", width=150, anchor="center")
        self.tree.column("Type", width=250, anchor="w")
        self.tree.column("Duration", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Первоначальный вывод данных в таблицу
        self.update_table()

    def add_training(self):
        date_str = self.entry_date.get().strip()
        t_type = self.entry_type.get().strip()
        duration = self.entry_duration.get().strip()

        # Простая проверка на заполнение полей
        if not date_str or not t_type or not duration:
            messagebox.showwarning("Ошибка ввода", "Пожалуйста, заполните все поля!")
            return

        new_training = {"date": date_str, "type": t_type, "duration": duration}

        self.trainings.append(new_training)
        self.save_data()
        self.update_table()
        self.clear_form()

    def clear_form(self):
        # Очистка полей ввода (кроме даты для удобства повторного ввода)
        self.entry_type.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)

    def update_table(self):
        # Очищаем таблицу перед обновлением
        for item in self.tree.get_children():
            self.tree.delete(item)

        f_type = self.filter_type.get().lower().strip()
        f_date = self.filter_date.get().strip()

    def update_table(self):
        # Получаем значения фильтров (приведите к нижнему регистру для надежности)
        f_type = self.filter_type.get().lower()
        f_date = self.filter_date.get()

        # Обязательно очищаем таблицу перед заполнением!
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Логика фильтрации и вставки
        for t in self.trainings:
            if f_type and f_type not in t["type"].lower():
                continue
            if f_date and f_date not in t["date"]:
                continue
            
            # Вставка строки в таблицу
            self.tree.insert("", tk.END, values=(t["date"], t["type"], t["duration"]))

    def clear_filters(self):
        self.filter_type.delete(0, tk.END)
        self.filter_date.delete(0, tk.END)
        self.update_table()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_data(self):
        # Реализация сохранения данных (исправлен синтаксис)
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()
