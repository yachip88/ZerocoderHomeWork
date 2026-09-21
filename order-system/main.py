import sqlite3
from pathlib import Path
from tkinter import messagebox, ttk
import tkinter as tk

DB_PATH = Path(__file__).resolve().parent / "business_orders.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            order_details TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def add_order():
    name = customer_name_entry.get().strip()
    details = order_details_entry.get().strip()
    if not name or not details:
        messagebox.showwarning("Предупреждение", "Заполните имя клиента и детали заказа")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
        (name, details),
    )
    conn.commit()
    conn.close()

    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
    view_orders()


def view_orders():
    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()


def complete_order():
    selected_item = tree.selection()
    if selected_item:
        order_id = tree.item(selected_item, "values")[0]
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status='Завершён' WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для завершения")


app = tk.Tk()
app.title("Система управления заказами")
app.geometry("720x480")

tk.Label(app, text="Имя клиента").pack()
customer_name_entry = tk.Entry(app, width=60)
customer_name_entry.pack()

tk.Label(app, text="Детали заказа").pack()
order_details_entry = tk.Entry(app, width=60)
order_details_entry.pack()

add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack(pady=4)

complete_button = tk.Button(app, text="Завершить заказ", command=complete_order)
complete_button.pack(pady=4)

columns = ("id", "customer_name", "order_details", "status")
tree = ttk.Treeview(app, columns=columns, show="headings")
headings = {
    "id": "id",
    "customer_name": "customer_name",
    "order_details": "order_details",
    "status": "status",
}
for column in columns:
    tree.heading(column, text=headings[column])
    tree.column(column, width=160 if column != "id" else 60, anchor="w")
tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

init_db()
view_orders()
app.mainloop()
