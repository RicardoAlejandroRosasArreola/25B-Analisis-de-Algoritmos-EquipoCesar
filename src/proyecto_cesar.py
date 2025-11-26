import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import collections
import time
import tracemalloc

# Parte de las graficas
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


class CifradoCesar:
    def __init__(self):
        self.diccionario = set()

    def quitar_acentos(self, char):
        # Mapeo simple de vocales acentuadas a vocales normales
        # Esto permite que la matemática (a-z) funcione correctamente
        reemplazos = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u',  # Convierrte mayusculas a minusculas
            'ü': 'u', 'Ü': 'u'
        }
        return reemplazos.get(char, char)

    # Funcion para arreglar lo del codigo ASCII
    def ajustar_char(self, val):
        if (val >= 123): return val - 122 + 96
        if (val < 97 and val != 32): return val + 26
        return val

    # Funcion basica para descifrar con un salto especifico
    def descifrar_str(self, texto, salto):
        res = []
        for letra in texto:
            # quitamos acento si tiene
            letra_norm = self.quitar_acentos(letra)

            # Verificamos si es letra valida
            if letra_norm.isalpha():
                c = int(ord(letra_norm))
                # Cuidado con la ñ
                if (c == 241 or c == 209):
                    c = self.ajustar_char(110 - salto)
                else:
                    c = self.ajustar_char(c - salto)
                res.append(chr(c))
            else:
                # Si no es letra (espacio, coma, numero), se agrega sin cambios
                res.append(letra)
        return "".join(res)

    def crear_cifrado(self, original):
        # Limpiamos el diccionario anterior
        self.diccionario.clear()

        # Guardamos las palabras del input para que los algoritmos las busquen
        palabras = original.split()
        for p in palabras:
            # Quitamos simbolos raros y dejamos solo letras
            # AQUI TAMBIEN: Normalizamos antes de guardar en el diccionario
            p_temp = ""
            for char in p:
                p_temp += self.quitar_acentos(char)

            palab_limpia = ''.join(filter(str.isalpha, p_temp)).lower()

            if len(palab_limpia) >= 2:  # Guardamos palabras de 2 letras o mas
                self.diccionario.add(palab_limpia)

        cifrado = []
        salto = random.randint(1, 25)
        original_min = original.lower()

        for l in original_min:
            # Normalizamos la letra actual del input
            l_norm = self.quitar_acentos(l)

            # Verificamos si es alfabético
            if l_norm.isalpha():
                val = int(ord(l_norm))
                if (val == 241 or val == 209):
                    val = self.ajustar_char(110 + salto)
                else:
                    val = self.ajustar_char(val + salto)
                cifrado.append(chr(val))
            else:
                # Dejamos simbolos y numeros igual
                cifrado.append(l)

        return "".join(cifrado), salto

    # Funcion para medir rendimiento
    def medir(self, funcion, *args):
        tracemalloc.start()
        t_inicio = time.perf_counter_ns()

        resultado = funcion(*args)

        t_fin = time.perf_counter_ns()
        _, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        total_time = t_fin - t_inicio
        return resultado, total_time, pico

    # --- ALGORITMOS ---

    def fuerza_bruta(self, cifrado):
        lista = []
        for i in range(1, 26):
            dec = self.descifrar_str(cifrado, i)
            lista.append(f"Salto {i:02d}: {dec}")
        return lista

    def divide_y_venceras(self, cifrado):
        n = len(cifrado)
        mitad = n // 2
        parte1 = cifrado[:mitad]

        mejor_salto = 0
        max_aciertos = -1

        for i in range(1, 26):
            texto_temp = self.descifrar_str(parte1, i)
            palabras = texto_temp.split()
            aciertos = 0

            for p in palabras:
                # Limpieza para comparar con diccionario
                p_norm = ""
                for char in p: p_norm += self.quitar_acentos(char)
                palab_limpia = ''.join(filter(str.isalpha, p_norm)).lower()

                if palab_limpia in self.diccionario:
                    aciertos += 1

            if aciertos > max_aciertos:
                max_aciertos = aciertos
                mejor_salto = i

        final = self.descifrar_str(cifrado, mejor_salto)
        return [f"Salto detectado (DyV): {mejor_salto} -> {final}"]

    def algoritmo_voraz(self, cifrado):
        # Limpiamos el texto cifrado para el analisis de frecuencia
        txt_limpio = "".join(filter(str.isalpha, cifrado.lower()))
        conteo = collections.Counter(txt_limpio)

        if not conteo: return ["Error: texto sin letras"]

        top_letras = [x[0] for x in conteo.most_common(3)]
        mejor_texto = "No se encontró solución lógica"
        max_aciertos = 0
        candidatos = ['e', 'a', 'o', 's', 'n']

        for letra_cifrada in top_letras:
            if ord(letra_cifrada) > 122: continue

            for meta in candidatos:
                dif = (ord(letra_cifrada) - ord(meta)) % 26
                if dif == 0: dif = 26

                intento = self.descifrar_str(cifrado, dif)

                aciertos = 0
                for pal in intento.split():
                    # Limpieza para comparar
                    p_norm = ""
                    for char in pal: p_norm += self.quitar_acentos(char)
                    pal_limpia = ''.join(filter(str.isalpha, p_norm)).lower()

                    if len(pal_limpia) > 1 and pal_limpia in self.diccionario:
                        aciertos += 1

                if aciertos > max_aciertos:
                    max_aciertos = aciertos
                    mejor_texto = intento

        if max_aciertos == 0:
            return ["Fallo Voraz: No coincidió con el diccionario (intenta texto más largo)"]

        return [f"Mejor intento Voraz: {mejor_texto}"]

    def branch_and_bound(self, cifrado):
        validos = []
        for i in range(1, 26):
            completo = self.descifrar_str(cifrado, i)
            palabras = completo.split()
            aciertos = 0
            revisadas = 0

            for pal in palabras:
                # Limpieza para comparar
                p_norm = ""
                for char in pal: p_norm += self.quitar_acentos(char)
                palabra_limpia = ''.join(filter(str.isalpha, p_norm)).lower()

                if len(palabra_limpia) < 3: continue
                revisadas += 1

                if palabra_limpia in self.diccionario:
                    aciertos += 1

            if revisadas > 0 and aciertos == 0:
                continue

            validos.append(f"Salto {i}: {completo}")
        return validos


# ================= INTERFAZ GRAFICA (Igual que antes) =============

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorítmica - Cifrado César (Soporte Acentos)")
        self.root.geometry("950x750")

        self.logica = CifradoCesar()
        self.txt_cifrado = ""

        # --- ARRIBA ---
        frm_top = ttk.LabelFrame(self.root, text="Entrada de Datos")
        frm_top.pack(padx=10, pady=10, fill="x")

        ttk.Label(frm_top, text="Escribe una frase:").pack(anchor="w", padx=10)
        self.entrada = ttk.Entry(frm_top, width=70)
        self.entrada.pack(pady=5, padx=10)

        btn_gen = ttk.Button(frm_top, text="Generar Cifrado", command=self.hacer_cifrado)
        btn_gen.pack(pady=5)

        self.lbl_info = ttk.Label(frm_top, text="...", foreground="gray")
        self.lbl_info.pack(pady=5)

        # --- ALGORITMOS ---
        frm_bot = ttk.LabelFrame(self.root, text="Selección de Algoritmo")
        frm_bot.pack(padx=10, pady=5, fill="x")

        box = ttk.Frame(frm_bot)
        box.pack(pady=5)

        ttk.Button(box, text="1. Fuerza Bruta", command=lambda: self.correr_algo(1)).grid(row=0, column=0, padx=5)
        ttk.Button(box, text="2. Divide y Vencerás", command=lambda: self.correr_algo(2)).grid(row=0, column=1, padx=5)
        ttk.Button(box, text="3. Voraz (Greedy)", command=lambda: self.correr_algo(3)).grid(row=0, column=2, padx=5)
        ttk.Button(box, text="4. Branch & Bound", command=lambda: self.correr_algo(4)).grid(row=0, column=3, padx=5)

        ttk.Separator(frm_bot, orient='horizontal').pack(fill='x', pady=10)

        btn_plot = ttk.Button(frm_bot, text="VER GRÁFICAS DE RENDIMIENTO", command=self.graficar)
        btn_plot.pack(pady=5, fill='x', padx=40)

        # --- RESULTADOS ---
        frm_out = ttk.LabelFrame(self.root, text="Resultados")
        frm_out.pack(padx=10, pady=10, fill="both", expand=True)

        self.area_texto = scrolledtext.ScrolledText(frm_out, height=10)
        self.area_texto.pack(fill="both", expand=True, padx=5, pady=5)

        self.lbl_stats = ttk.Label(frm_out, text="Tiempo: -- | Memoria: --")
        self.lbl_stats.pack(anchor="e", padx=5)

    def hacer_cifrado(self):
        txt = self.entrada.get()
        if not txt:
            messagebox.showwarning("Error", "Escribe texto")
            return

        res, sal = self.logica.crear_cifrado(txt)
        self.txt_cifrado = res
        self.lbl_info.config(text=f"Texto Cifrado: {res} (Salto real: {sal})", foreground="blue")

        self.area_texto.delete(1.0, tk.END)
        self.area_texto.insert(tk.END, "Caso generado. Elige un algoritmo.\n")

    def correr_algo(self, op):
        if not self.txt_cifrado:
            messagebox.showerror("Error", "Genera el cifrado primero")
            return

        self.area_texto.delete(1.0, tk.END)
        resultado = None
        t, m = 0, 0
        titulo = ""

        if op == 1:
            titulo = "Fuerza Bruta"
            resultado, t, m = self.logica.medir(self.logica.fuerza_bruta, self.txt_cifrado)
        elif op == 2:
            titulo = "Divide y Vencerás"
            resultado, t, m = self.logica.medir(self.logica.divide_y_venceras, self.txt_cifrado)
        elif op == 3:
            titulo = "Voraz"
            resultado, t, m = self.logica.medir(self.logica.algoritmo_voraz, self.txt_cifrado)
        elif op == 4:
            titulo = "Branch & Bound"
            resultado, t, m = self.logica.medir(self.logica.branch_and_bound, self.txt_cifrado)

        self.area_texto.insert(tk.END, f"=== {titulo} ===\n\n")
        if isinstance(resultado, list):
            for linea in resultado:
                self.area_texto.insert(tk.END, linea + "\n")
        else:
            self.area_texto.insert(tk.END, str(resultado) + "\n")

        self.lbl_stats.config(text=f"Tiempo: {t} ns | Memoria: {m} bytes")

    def graficar(self):
        if not self.txt_cifrado:
            messagebox.showerror("Error", "Sin datos para graficar")
            return

        nombres = ["F. Bruta", "DyV", "Voraz", "B&B"]

        _, t1, m1 = self.logica.medir(self.logica.fuerza_bruta, self.txt_cifrado)
        _, t2, m2 = self.logica.medir(self.logica.divide_y_venceras, self.txt_cifrado)
        _, t3, m3 = self.logica.medir(self.logica.algoritmo_voraz, self.txt_cifrado)
        _, t4, m4 = self.logica.medir(self.logica.branch_and_bound, self.txt_cifrado)

        tiempos = [t1, t2, t3, t4]
        mems = [m1, m2, m3, m4]

        top = tk.Toplevel(self.root)
        top.title("Rendimiento")
        top.geometry("900x500")

        figura = Figure(figsize=(10, 5), dpi=100)

        ax1 = figura.add_subplot(121)
        barras1 = ax1.bar(nombres, tiempos, color='#5DADE2')
        ax1.set_title('Tiempo (ns)')
        for b in barras1:
            h = b.get_height()
            ax1.text(b.get_x() + b.get_width() / 2., h, f'{int(h)}', ha='center', va='bottom', fontsize=9)

        ax2 = figura.add_subplot(122)
        barras2 = ax2.bar(nombres, mems, color='#58D68D')
        ax2.set_title('Memoria (bytes)')
        for b in barras2:
            h = b.get_height()
            ax2.text(b.get_x() + b.get_width() / 2., h, f'{int(h)}', ha='center', va='bottom', fontsize=9)

        figura.tight_layout()
        canvas = FigureCanvasTkAgg(figura, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    ventana = tk.Tk()
    app = MainApp(ventana)
    ventana.mainloop()