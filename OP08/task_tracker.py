import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class TaskTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер Задач")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Цветовая схема
        self.bg_color = "#1a1a2e"
        self.secondary_bg = "#16213e"
        self.accent_color = "#0f3460"
        self.highlight_color = "#e94560"
        self.text_color = "#eaeaea"
        self.success_color = "#4CAF50"
        
        self.root.configure(bg=self.bg_color)
        
        self.tasks = []
        self.load_tasks()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Заголовок
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=20, padx=20, fill="x")
        
        title_label = tk.Label(
            header_frame,
            text="📋 Мои Задачи",
            font=("Segoe UI", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text=f"Всего задач: {len(self.tasks)}",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.text_color
        )
        subtitle_label.pack()
        
        # Поле ввода новой задачи
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10, padx=20, fill="x")
        
        self.task_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg=self.secondary_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat",
            bd=0
        )
        self.task_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        add_button = tk.Button(
            input_frame,
            text="➕ Добавить",
            font=("Segoe UI", 11, "bold"),
            bg=self.highlight_color,
            fg=self.text_color,
            activebackground="#d63447",
            activeforeground=self.text_color,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.add_task
        )
        add_button.pack(side="right", ipady=8, ipadx=15)
        
        # Контейнер для списка задач
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Canvas и Scrollbar для прокрутки
        canvas = tk.Canvas(list_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        
        self.tasks_container = tk.Frame(canvas, bg=self.bg_color)
        self.tasks_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.tasks_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Настройка стиля scrollbar
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Vertical.TScrollbar",
            background=self.secondary_bg,
            troughcolor=self.bg_color,
            bordercolor=self.bg_color,
            arrowcolor=self.text_color
        )
        
        # Футер со статистикой
        footer_frame = tk.Frame(self.root, bg=self.secondary_bg)
        footer_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        self.stats_label = tk.Label(
            footer_frame,
            text="",
            font=("Segoe UI", 9),
            bg=self.secondary_bg,
            fg=self.text_color,
            pady=10
        )
        self.stats_label.pack()
        
        self.refresh_tasks()
        
    def add_task(self):
        task_text = self.task_entry.get().strip()
        
        if task_text:
            task = {
                "text": task_text,
                "completed": False
            }
            self.tasks.append(task)
            self.save_tasks()
            self.task_entry.delete(0, tk.END)
            self.refresh_tasks()
        else:
            messagebox.showwarning("Внимание", "Введите текст задачи!")
            
    def toggle_task(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_tasks()
        self.refresh_tasks()
        
    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()
        self.refresh_tasks()
        
    def refresh_tasks(self):
        # Очистка контейнера
        for widget in self.tasks_container.winfo_children():
            widget.destroy()
            
        # Создание элементов задач
        for i, task in enumerate(self.tasks):
            self.create_task_widget(i, task)
            
        # Обновление статистики
        completed = sum(1 for task in self.tasks if task["completed"])
        total = len(self.tasks)
        self.stats_label.config(
            text=f"Выполнено: {completed} из {total}"
        )
        
        # Обновление заголовка
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and "Всего задач" in child.cget("text"):
                        child.config(text=f"Всего задач: {total}")
                        
    def create_task_widget(self, index, task):
        task_frame = tk.Frame(
            self.tasks_container,
            bg=self.secondary_bg,
            pady=10,
            padx=15
        )
        task_frame.pack(fill="x", pady=5, padx=5)
        
        # Чекбокс
        check_var = tk.BooleanVar(value=task["completed"])
        check_button = tk.Checkbutton(
            task_frame,
            variable=check_var,
            bg=self.secondary_bg,
            activebackground=self.secondary_bg,
            selectcolor=self.accent_color,
            command=lambda: self.toggle_task(index),
            cursor="hand2"
        )
        check_button.pack(side="left", padx=(0, 10))
        
        # Текст задачи
        text_style = ("Segoe UI", 11)
        if task["completed"]:
            text_style = ("Segoe UI", 11, "overstrike")
            text_fg = "#888888"
        else:
            text_fg = self.text_color
            
        task_label = tk.Label(
            task_frame,
            text=task["text"],
            font=text_style,
            bg=self.secondary_bg,
            fg=text_fg,
            anchor="w"
        )
        task_label.pack(side="left", fill="x", expand=True)
        
        # Кнопка удаления
        delete_button = tk.Button(
            task_frame,
            text="🗑️",
            font=("Segoe UI", 12),
            bg=self.secondary_bg,
            fg=self.highlight_color,
            activebackground=self.accent_color,
            activeforeground=self.highlight_color,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: self.delete_task(index)
        )
        delete_button.pack(side="right")
        
    def save_tasks(self):
        try:
            with open("tasks.json", "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить задачи: {e}")
            
    def load_tasks(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить задачи: {e}")
                self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskTracker(root)
    root.mainloop()
