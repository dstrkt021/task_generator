import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Файлы
TASKS_FILE = "tasks_data.json"
HISTORY_FILE = "history_data.json"


class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("850x650")
        self.root.resizable(False, False)

        # Базовые задачи
        self.default_tasks = {
            "Учёба": [
                "Прочитать статью",
                "Выучить 10 новых слов",
                "Решить 5 задач по математике"
            ],
            "Спорт": [
                "Сделать зарядку",
                "Пробежать 2 км",
                "10 минут растяжки"
            ],
            "Работа": [
                "Проверить почту",
                "Закончить проект",
                "Сделать отчёт"
            ]
        }

        self.tasks = {}
        self.history = []

        # Загрузка данных
        self.load_tasks()
        self.load_history()

        # Интерфейс
        self.create_widgets()

    # ---------------------------
    # GUI
    # ---------------------------
    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Random Task Generator",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)

        # Фильтр категории
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Выберите категорию:").pack(side=tk.LEFT, padx=5)

        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.category_var,
            values=["Все", "Учёба", "Спорт", "Работа"],
            state="readonly",
            width=20
        )
        self.category_combo.current(0)
        self.category_combo.pack(side=tk.LEFT)

        # Генерация задачи
        generate_btn = tk.Button(
            self.root,
            text="Сгенерировать задачу",
            font=("Arial", 12),
            bg="lightgreen",
            command=self.generate_task
        )
        generate_btn.pack(pady=10)

        self.result_label = tk.Label(
            self.root,
            text="Нажмите кнопку для генерации",
            font=("Arial", 14),
            fg="blue",
            wraplength=700
        )
        self.result_label.pack(pady=10)

        # Добавление новой задачи
        add_frame = tk.LabelFrame(self.root, text="Добавить новую задачу")
        add_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(add_frame, text="Название задачи:").grid(row=0, column=0, padx=5, pady=5)

        self.new_task_entry = tk.Entry(add_frame, width=45)
        self.new_task_entry.grid(row=0, column=1, padx=5)

        tk.Label(add_frame, text="Категория:").grid(row=1, column=0, padx=5, pady=5)

        self.new_task_category = ttk.Combobox(
            add_frame,
            values=["Учёба", "Спорт", "Работа"],
            state="readonly"
        )
        self.new_task_category.current(0)
        self.new_task_category.grid(row=1, column=1, padx=5)

        add_btn = tk.Button(
            add_frame,
            text="Добавить задачу",
            bg="lightyellow",
            command=self.add_task
        )
        add_btn.grid(row=2, column=1, pady=10)

        # Список пользовательских задач
        user_tasks_frame = tk.LabelFrame(self.root, text="Список всех задач")
        user_tasks_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tasks_listbox = tk.Listbox(user_tasks_frame, width=90, height=10)
        self.tasks_listbox.pack(side=tk.LEFT, fill="both", expand=True)

        tasks_scrollbar = tk.Scrollbar(user_tasks_frame)
        tasks_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.tasks_listbox.config(yscrollcommand=tasks_scrollbar.set)
        tasks_scrollbar.config(command=self.tasks_listbox.yview)

        # Удаление задачи
        delete_btn = tk.Button(
            self.root,
            text="Удалить выбранную задачу",bg="tomato",
            fg="white",
            command=self.delete_task
        )
        delete_btn.pack(pady=5)

        # История
        history_frame = tk.LabelFrame(self.root, text="История сгенерированных задач")
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.history_listbox = tk.Listbox(history_frame, width=90, height=8)
        self.history_listbox.pack(side=tk.LEFT, fill="both", expand=True)

        history_scrollbar = tk.Scrollbar(history_frame)
        history_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.history_listbox.config(yscrollcommand=history_scrollbar.set)
        history_scrollbar.config(command=self.history_listbox.yview)

        # Заполнение данных
        self.refresh_tasks_list()
        self.refresh_history_list()

        # Кнопки сохранения
        save_frame = tk.Frame(self.root)
        save_frame.pack(pady=10)

        tk.Button(
            save_frame,
            text="Сохранить задачи",
            bg="lightblue",
            command=self.save_tasks
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            save_frame,
            text="Сохранить историю",
            bg="lightblue",
            command=self.save_history
        ).pack(side=tk.LEFT, padx=10)

    # ---------------------------
    # Работа с задачами
    # ---------------------------
    def generate_task(self):
        category = self.category_var.get()

        available_tasks = []

        if category == "Все":
            for cat, tasks in self.tasks.items():
                for task in tasks:
                    available_tasks.append((cat, task))
        else:
            for task in self.tasks.get(category, []):
                available_tasks.append((category, task))

        if not available_tasks:
            messagebox.showwarning("Нет задач", "В выбранной категории нет задач.")
            return

        selected_category, selected_task = random.choice(available_tasks)

        task_text = f"[{selected_category}] {selected_task}"

        self.result_label.config(text=task_text)

        self.history.append(task_text)
        self.history_listbox.insert(tk.END, task_text)

        self.save_history()

    def add_task(self):
        task = self.new_task_entry.get().strip()
        category = self.new_task_category.get()

        if not task:
            messagebox.showerror("Ошибка", "Задача не может быть пустой!")
            return

        if task in self.tasks[category]:
            messagebox.showwarning("Ошибка", "Такая задача уже существует.")
            return

        self.tasks[category].append(task)

        self.new_task_entry.delete(0, tk.END)

        self.refresh_tasks_list()
        self.save_tasks()

        messagebox.showinfo("Успех", "Задача успешно добавлена!")

    def delete_task(self):
        selected = self.tasks_listbox.curselection()

        if not selected:
            messagebox.showwarning("Ошибка", "Выберите задачу для удаления.")
            return

        selected_text = self.tasks_listbox.get(selected[0])

        try:
            category = selected_text.split("]")[0][1:]
            task = selected_text.split("] ")[1]

            if task in self.tasks[category]:
                self.tasks[category].remove(task)

            self.refresh_tasks_list()
            self.save_tasks()

            messagebox.showinfo("Удалено", "Задача удалена.")

        except Exception:
            messagebox.showerror("Ошибка", "Не удалось удалить задачу.")

    # ---------------------------
    # Отображение
    # ---------------------------
    def refresh_tasks_list(self):
        self.tasks_listbox.delete(0, tk.END)

        for category, tasks in self.tasks.items():
            for task in tasks:
                self.tasks_listbox.insert(tk.END, f"[{category}] {task}")

    def refresh_history_list(self):
        self.history_listbox.delete(0, tk.END)

        for task in self.history:
            self.history_listbox.insert(tk.END, task)

    # ---------------------------
    # JSON сохранение# ---------------------------
    def save_tasks(self):
        try:
            with open(TASKS_FILE, "w", encoding="utf-8") as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения задач:\n{e}")

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, "r", encoding="utf-8") as file:
                    self.tasks = json.load(file)
            except:
                self.tasks = self.default_tasks.copy()
        else:
            self.tasks = self.default_tasks.copy()
            self.save_tasks()

    def save_history(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                json.dump(self.history, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения истории:\n{e}")

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                    self.history = json.load(file)
            except:
                self.history = []
        else:
            self.history = []
            self.save_history()


# ---------------------------
# Запуск программы
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()