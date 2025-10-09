import tkinter as tk
from tkinter import ttk
import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

DB = config["DATABASE"]

def conectar():
    host = entry_host.get() or DB["host"]
    user = entry_user.get() or DB["user"]
    password = entry_pass.get() or DB["password"]
    database = entry_db.get() or DB["database"]

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

def cargar_tablas():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    combo_tablas["values"] = [t[0] for t in cur.fetchall()]
    conn.close()

def mostrar_registros():
    tabla = combo_tablas.get()
    conn = conectar()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {tabla}")
    datos = cur.fetchall()
    cols = [c[0] for c in cur.description]

    tree.delete(*tree.get_children())
    tree["columns"] = cols
    tree["show"] = "headings"
    for c in cols:
        tree.heading(c, text=c)
    for fila in datos:
        tree.insert("", "end", values=fila)
    conn.close()

root = tk.Tk()
root.title("Visor MySQL Simple")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

ttk.Label(frame, text="Host:").grid(row=0, column=0, sticky="e")
entry_host = ttk.Entry(frame)
entry_host.insert(0, DB["host"])
entry_host.grid(row=0, column=1)

ttk.Label(frame, text="Usuario:").grid(row=1, column=0, sticky="e")
entry_user = ttk.Entry(frame)
entry_user.insert(0, DB["user"])
entry_user.grid(row=1, column=1)

ttk.Label(frame, text="Contraseña:").grid(row=2, column=0, sticky="e")
entry_pass = ttk.Entry(frame, show="*")
entry_pass.insert(0, DB["password"])
entry_pass.grid(row=2, column=1)

ttk.Label(frame, text="Base de datos:").grid(row=3, column=0, sticky="e")
entry_db = ttk.Entry(frame)
entry_db.insert(0, DB["database"])
entry_db.grid(row=3, column=1)

# BOTONES
ttk.Button(root, text="Cargar Tablas", command=cargar_tablas).pack(pady=5)
combo_tablas = ttk.Combobox(root)
combo_tablas.pack(pady=5)
ttk.Button(root, text="Mostrar Registros", command=mostrar_registros).pack(pady=5)

tree = ttk.Treeview(root)
tree.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()
