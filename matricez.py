import tkinter as tk
import numpy as np
from numpy.linalg import inv, det
from tkinter import messagebox

def encontrar_inversa():
    matriz = obtener_matriz()
    try:
        inversa = inv(matriz)
        mostrar_resultado("Inversa de la matriz", inversa)
    except np.linalg.LinAlgError:
        mostrar_error("La matriz no tiene inversa")

def multiplicar_matrices():
    matriz1 = obtener_matriz("Matriz 1")
    matriz2 = obtener_matriz("Matriz 2")

    try:
        resultado = np.dot(matriz1, matriz2)
        mostrar_resultado("Multiplicación de matrices", resultado)
    except ValueError:
        mostrar_error("La multiplicación no es posible")

def resolver_sistema(method):
    if method == "Gauss-Jordan":
        resolver_sistema_gauss_jordan()
    elif method == "Cramer":
        resolver_sistema_cramer()

def resolver_sistema_gauss_jordan():
    matriz = obtener_matriz("Matriz de coeficientes")
    resultados = obtener_matriz("Matriz de resultados")

    try:
        solucion = np.linalg.solve(matriz, resultados)
        mostrar_resultado("Solución del sistema de ecuaciones", solucion)
    except np.linalg.LinAlgError:
        mostrar_error("No se puede resolver el sistema de ecuaciones")

def resolver_sistema_cramer():
    matriz = obtener_matriz("Matriz de coeficientes")
    resultados = obtener_matriz("Matriz de resultados")

    det_matriz = det(matriz)

    if det_matriz == 0:
        mostrar_error("El determinante de la matriz de coeficientes es cero. No se puede resolver usando la regla de Cramer.")
        return

    n = matriz.shape[0]
    soluciones = []

    for i in range(n):
        matriz_temporal = matriz.copy()
        matriz_temporal[:, i] = resultados
        soluciones.append(round(det(matriz_temporal) / det_matriz, 2))

    mostrar_resultado("Solución del sistema de ecuaciones (Cramer)", soluciones)

def obtener_matriz(titulo="Ingrese la matriz"):
    entrada_matriz = MatrizEntrada(titulo)
    entrada_matriz.wait_window()
    return entrada_matriz.matriz

def mostrar_resultado(titulo, resultado):
    resultado_ventana = ResultadoVentana(titulo, resultado)
    resultado_ventana.wait_window()

def mostrar_error(mensaje):
    messagebox.showerror("Error", mensaje)

class MatrizEntrada(tk.Toplevel):
    def __init__(self, titulo):
        super().__init__()

        self.matriz = None

        self.title(titulo)

        self.etiquetas = []
        self.entradas = []

        self.crear_entrada_matriz()

    def crear_entrada_matriz(self):
        tk.Label(self, text="Ingrese los valores de la matriz:").pack()

        self.frame = tk.Frame(self)
        self.frame.pack()

        self.fila_columna_frame = tk.Frame(self)
        self.fila_columna_frame.pack()

        tk.Label(self.fila_columna_frame, text="Filas:").pack(side=tk.LEFT)
        self.filas_entry = tk.Entry(self.fila_columna_frame)
        self.filas_entry.pack(side=tk.LEFT)

        tk.Label(self.fila_columna_frame, text="Columnas:").pack(side=tk.LEFT)
        self.columnas_entry = tk.Entry(self.fila_columna_frame)
        self.columnas_entry.pack(side=tk.LEFT)

        tk.Button(self, text="Aceptar", font=("Arial", 12), bg="black", fg="white", command=self.obtener_valores).pack()

    def obtener_valores(self):
        try:
            filas = int(self.filas_entry.get())
            columnas = int(self.columnas_entry.get())

            self.etiquetas = []
            self.entradas = []
            
            for i in range(filas):
                fila = tk.Frame(self.frame)
                fila.pack()
                self.etiquetas.append([])
                self.entradas.append([])

                for j in range(columnas):
                    etiqueta = tk.Label(fila, text=f"Fila {i+1}, Col {j+1}:")
                    etiqueta.pack(side=tk.LEFT)
                    self.etiquetas[i].append(etiqueta)

                    entrada = tk.Entry(fila)
                    entrada.pack(side=tk.LEFT)
                    self.entradas[i].append(entrada)

            tk.Button(self, text="Calcular", font=("Arial", 12), bg="black", fg="white", command=self.obtener_matriz_resultado).pack()

        except ValueError:
            mostrar_error("Ingrese valores válidos para filas y columnas")

    def obtener_matriz_resultado(self):
        try:
            filas = len(self.entradas)
            columnas = len(self.entradas[0])

            matriz = []

            for i in range(filas):
                fila = []
                for j in range(columnas):
                    valor = float(self.entradas[i][j].get())
                    fila.append(valor)
                matriz.append(fila)

            self.matriz = np.array(matriz)
            self.destroy()

        except ValueError:
            mostrar_error("Ingrese valores numéricos válidos")

class ResultadoVentana(tk.Toplevel):
    def __init__(self, titulo, resultado):
        super().__init__()

        self.title(titulo)

        tk.Label(self, text=titulo).pack()

        texto_resultado = tk.Text(self, height=10, width=40)
        texto_resultado.pack()
        texto_resultado.insert(tk.END, str(resultado))

# Crear la ventana principal
root = tk.Tk()
root.title("Operaciones Matriciales")

# Botones para las operaciones
inversa_button = tk.Button(root, text="Encontrar Inversa", font=("Arial", 12), command=encontrar_inversa, padx=10, pady=20, bg="red", fg="white")
inversa_button.pack()

multiplicacion_button = tk.Button(root, text="Multiplicar Matrices", font=("Arial", 12), command=multiplicar_matrices, pady=20, bg="green", fg="white")
multiplicacion_button.pack()

resolver_gauss_button = tk.Button(root, text="Resolver Sistema de Ecuaciones (Gauss-Jordan)", font=("Arial", 12), command=lambda: resolver_sistema("Gauss-Jordan"), pady=20, bg="yellow")
resolver_gauss_button.pack()

resolver_cramer_button = tk.Button(root, text="Resolver Sistema de Ecuaciones (Cramer)", font=("Arial", 12), command=lambda: resolver_sistema("Cramer"), pady=20, bg="blue", fg="white")
resolver_cramer_button.pack()

root.mainloop()