import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Plotter")

        # File Selection
        self.file_path = tk.StringVar()
        self.create_file_browser()

        # Data Preview
        self.data_frame = None
        self.create_data_preview()

        # Plot Options
        self.x_column = tk.StringVar()
        self.y_column = tk.StringVar()
        self.plot_type = tk.StringVar(value="Line")
        self.create_plot_options()

        # Plot Display
        self.plot_area = None
        self.create_plot_display()

    def create_file_browser(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="x")

        ttk.Label(frame, text="File:").pack(side="left", padx=5)
        ttk.Entry(frame, textvariable=self.file_path, width=50, state="readonly").pack(side="left", padx=5)
        ttk.Button(frame, text="Browse", command=self.browse_file).pack(side="left", padx=5)

    def create_data_preview(self):
        frame = ttk.LabelFrame(self.root, text="Data Preview", padding=10)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.text_preview = tk.Text(frame, wrap="none", height=10, state="disabled")
        self.text_preview.pack(fill="both", expand=True)

    def create_plot_options(self):
        frame = ttk.LabelFrame(self.root, text="Plot Options", padding=10)
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="X Column:").grid(row=0, column=0, padx=5, pady=5)
        self.x_menu = ttk.OptionMenu(frame, self.x_column, None)
        self.x_menu.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Y Column:").grid(row=0, column=2, padx=5, pady=5)
        self.y_menu = ttk.OptionMenu(frame, self.y_column, None)
        self.y_menu.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Plot Type:").grid(row=0, column=4, padx=5, pady=5)
        plot_types = ["Line", "Scatter", "Bar"]
        ttk.OptionMenu(frame, self.plot_type, "Line", *plot_types).grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(frame, text="Plot", command=self.plot_data).grid(row=0, column=6, padx=5, pady=5)

    def create_plot_display(self):
        frame = ttk.LabelFrame(self.root, text="Plot", padding=10)
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.plot_area = frame

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"), ("Text Files", "*.txt")]
        )
        if file_path:
            self.file_path.set(file_path)
            self.load_data(file_path)

    def load_data(self, file_path):
        try:
            if file_path.endswith(".csv"):
                self.data_frame = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                self.data_frame = pd.read_excel(file_path)
            else:
                messagebox.showerror("Invalid File", "Unsupported file format.")
                return

            # Preview data
            self.text_preview.configure(state="normal")
            self.text_preview.delete(1.0, tk.END)
            self.text_preview.insert(tk.END, self.data_frame.head().to_string())
            self.text_preview.configure(state="disabled")

            # Update column selection
            columns = self.data_frame.columns.tolist()
            self.update_column_options(columns)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def update_column_options(self, columns):
        menu = self.x_menu["menu"]
        menu.delete(0, "end")
        for col in columns:
            menu.add_command(label=col, command=lambda value=col: self.x_column.set(value))

        menu = self.y_menu["menu"]
        menu.delete(0, "end")
        for col in columns:
            menu.add_command(label=col, command=lambda value=col: self.y_column.set(value))

    def plot_data(self):
        if self.data_frame is None:  # Corregido
            messagebox.showerror("Error", "No data loaded.")
            return
        if not self.x_column.get() or not self.y_column.get():
            messagebox.showerror("Error", "Please select both X and Y columns.")
            return

        try:
            x = self.data_frame[self.x_column.get()]
            y = self.data_frame[self.y_column.get()]
            plot_type = self.plot_type.get()

            fig, ax = plt.subplots(figsize=(6, 4))
            if plot_type == "Line":
                ax.plot(x, y)
            elif plot_type == "Scatter":
                ax.scatter(x, y)
            elif plot_type == "Bar":
                ax.bar(x, y)

            ax.set_title("Data Plot")
            ax.set_xlabel(self.x_column.get())
            ax.set_ylabel(self.y_column.get())

            for widget in self.plot_area.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.plot_area)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to plot data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataPlotterApp(root)
    root.mainloop()




#Características del código:
#Navegación de Archivos: Permite seleccionar archivos CSV, Excel o TXT con un cuadro de diálogo.
#Vista Previa de Datos: Muestra las primeras filas del archivo cargado en un área de texto.
#Selección Dinámica de Columnas: Los menús desplegables se actualizan automáticamente según las columnas del archivo cargado.
#Opciones de Gráfica: Permite elegir entre gráficos de línea, dispersión o barras.
#Gráfica Embebida: Las gráficas se muestran dentro de la ventana principal utilizando Matplotlib.
#Prueba este código y ajusta cualquier detalle según tus necesidades.
