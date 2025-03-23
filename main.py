"""
Autor: Harry fishet lasso hernandez 
Descripción: Aplicación para cargar, visualizar y graficar datos de un archivo CSV.
"""

import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def cargar_csv():
    """Carga un archivo CSV y muestra los datos en un Treeview."""
    global data
    file_path = filedialog.askopenfilename(title="Selecciona un archivo CSV", filetypes=[("Archivos CSV", "*.csv")])
    
    if not file_path:
        messagebox.showinfo("Información", "No se seleccionó ningún archivo.")
        return

    try:
        data = pd.read_csv(file_path)

        if data.empty:
            raise ValueError("El archivo CSV está vacío.")

        # Limpiar el Treeview antes de cargar nuevos datos
        for item in tree.get_children():
            tree.delete(item)

        # Configurar las columnas del Treeview
        tree["columns"] = list(data.columns)
        tree["show"] = "headings"

        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Insertar los datos en el Treeview
        for _, row in data.iterrows():
            tree.insert("", tk.END, values=list(row))

        messagebox.showinfo("Éxito", "Archivo CSV cargado correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo CSV.\nDetalles: {e}")

def graficar_datos():
    """Permite seleccionar columnas y graficar los datos dentro de la aplicación."""
    if data is None:
        messagebox.showwarning("Advertencia", "Primero debes cargar un archivo CSV.")
        return

    def crear_grafico():
        x_col = x_var.get()
        y_col = y_var.get()

        if x_col in data.columns and y_col in data.columns:
            # Crear figura de Matplotlib
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(data[x_col], data[y_col], marker='o', color="#4CAF50")
            ax.set_title(f'Gráfico de {y_col} vs {x_col}', fontsize=14)
            ax.set_xlabel(x_col, fontsize=12)
            ax.set_ylabel(y_col, fontsize=12)
            ax.grid(True)

            # Mostrar la gráfica en el canvas de Tkinter
            for widget in grafico_frame.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showerror("Error", "Selecciona columnas válidas para graficar.")

    grafico_window = tk.Toplevel(root)
    grafico_window.title("Seleccionar Columnas para Graficar")
    grafico_window.geometry("400x200")
    grafico_window.configure(bg="#f0f0f0")

    tk.Label(grafico_window, text="Columna para el eje X:", bg="#f0f0f0", fg="#333333").pack(pady=5)
    x_var = tk.StringVar(value=data.columns[0])
    x_menu = ttk.Combobox(grafico_window, textvariable=x_var, values=list(data.columns))
    x_menu.pack(pady=5)

    tk.Label(grafico_window, text="Columna para el eje Y:", bg="#f0f0f0", fg="#333333").pack(pady=5)
    y_var = tk.StringVar(value=data.columns[1])
    y_menu = ttk.Combobox(grafico_window, textvariable=y_var, values=list(data.columns))
    y_menu.pack(pady=5)

    tk.Button(grafico_window, text="Graficar", command=crear_grafico, bg="#4CAF50", fg="#ffffff").pack(pady=10)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Análisis de Datos CSV")
root.geometry("900x700")
root.configure(bg="#f0f0f0")

# Botones principales
frame_botones = tk.Frame(root, bg="#f0f0f0")
frame_botones.pack(side=tk.TOP, fill=tk.X, pady=10)

btn_cargar = tk.Button(frame_botones, text="Cargar CSV", command=cargar_csv, bg="#4CAF50", fg="#ffffff")
btn_cargar.pack(side=tk.LEFT, padx=5)

btn_graficar = tk.Button(frame_botones, text="Graficar Datos", command=graficar_datos, bg="#FF9800", fg="#ffffff")
btn_graficar.pack(side=tk.LEFT, padx=5)

# Treeview para mostrar los datos
tree_frame = tk.Frame(root, bg="#f0f0f0")
tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tree = ttk.Treeview(tree_frame)
tree.pack(fill=tk.BOTH, expand=True)

# Frame para mostrar la gráfica
grafico_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
grafico_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Variable global para almacenar los datos
data = None

# Iniciar la aplicación
root.mainloop()