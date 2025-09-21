import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
from typing import List, Dict

class CalculadoraTendenciaCentral:
    @staticmethod
    def texto_a_lista(texto: str) -> List[float]:
        if not texto.strip(): return []
        numeros = []
        for num_str in texto.replace(',', ' ').split():
            try: numeros.append(float(num_str))
            except: continue
        return numeros

    @staticmethod
    def calcular_media(datos: List[float]) -> float:
        return sum(datos) / len(datos) if datos else 0

    @staticmethod
    def calcular_mediana(datos: List[float]) -> float:
        if not datos: return 0
        datos_ordenados = sorted(datos)
        n = len(datos_ordenados)
        return (datos_ordenados[n//2 - 1] + datos_ordenados[n//2]) / 2 if n % 2 == 0 else datos_ordenados[n//2]

    @staticmethod
    def calcular_moda(datos: List[float]) -> List[float]:
        if not datos: return []
        frecuencias = {}
        for dato in datos: frecuencias[dato] = frecuencias.get(dato, 0) + 1
        max_frecuencia = max(frecuencias.values()) if frecuencias else 0
        return [dato for dato, freq in frecuencias.items() if freq == max_frecuencia]

    @staticmethod
    def calcular_desviacion_estandar(datos: List[float]) -> float:
        if len(datos) < 2: return 0
        media = CalculadoraTendenciaCentral.calcular_media(datos)
        return math.sqrt(sum((x - media) ** 2 for x in datos) / (len(datos) - 1))

    @staticmethod
    def calcular_rango(datos: List[float]) -> float:
        return max(datos) - min(datos) if datos else 0

    @staticmethod
    def calcular_cuartiles(datos: List[float]) -> Dict[str, float]:
        if not datos: return {"Q1": 0, "Q2": 0, "Q3": 0}
        datos_ordenados = sorted(datos)
        n = len(datos_ordenados)
        def percentil(p): return datos_ordenados[int((n - 1) * p / 100)]
        return {"Q1": percentil(25), "Q2": percentil(50), "Q3": percentil(75)}

    @staticmethod
    def calcular_numero_intervalos(datos: List[float]) -> int:
        """Calcula automáticamente el número de intervalos usando la regla de Sturges"""
        if not datos: return 5
        n = len(datos)
        return max(5, min(15, int(1 + 3.322 * math.log10(n))))

    @staticmethod
    def calcular_por_intervalos(datos: List[float]) -> Dict:
        if not datos: return {}
        num_intervalos = CalculadoraTendenciaCentral.calcular_numero_intervalos(datos)
        min_val, max_val, rango = min(datos), max(datos), max(datos) - min(datos)
        amplitud = math.ceil(rango / num_intervalos * 100) / 100  # Redondear hacia arriba a 2 decimales
        
        intervalos = []
        marcas_clase = []
        frecuencias = [0] * num_intervalos
        
        # Crear intervalos
        inicio = min_val
        for i in range(num_intervalos):
            fin = inicio + amplitud
            # Ajustar el último intervalo para incluir el valor máximo
            if i == num_intervalos - 1:
                fin = max_val + 0.01  # Pequeño ajuste para incluir el máximo
            intervalos.append((inicio, fin))
            marcas_clase.append((inicio + fin) / 2)
            inicio = fin
        
        # Contar frecuencias
        for dato in datos:
            for i, (inicio, fin) in enumerate(intervalos):
                if inicio <= dato < fin or (i == num_intervalos - 1 and dato <= fin):
                    frecuencias[i] += 1
                    break
        
        # Calcular frecuencias acumuladas y relativas
        facum = [sum(frecuencias[:i+1]) for i in range(num_intervalos)]
        frel = [freq / len(datos) for freq in frecuencias]
        media_aprox = sum(marca * freq for marca, freq in zip(marcas_clase, frecuencias)) / len(datos)
        
        return {
            "num_intervalos": num_intervalos,
            "amplitud": amplitud,
            "intervalos": intervalos,
            "marcas_clase": marcas_clase,
            "frecuencias": frecuencias,
            "frecuencias_acumuladas": facum,
            "frecuencias_relativas": frel,
            "media_aproximada": media_aprox
        }

class InterfazCalculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora medidas de tendencia central")
        self.root.geometry("800x600")
        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        ttk.Label(main_frame, text="Calculadora medidas de tendencia central", 
                 font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Button(main_frame, text="Cargar archivo de imagen con los datos", 
                  command=self.cargar_archivo).grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        
        ttk.Label(main_frame, text="O ingresa los datos manualmente (separados por comas):").grid(row=2, column=0, columnspan=2, sticky="w")
        
        self.entrada_datos = ttk.Entry(main_frame, width=50)
        self.entrada_datos.grid(row=3, column=0, columnspan=2, pady=(5, 10), sticky="ew")
        
        frame_botones = ttk.Frame(main_frame)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Button(frame_botones, text="Calcular por intervalos", 
                  command=self.calcular_intervalos).pack(side="left", padx=(0, 10))
        
        ttk.Button(frame_botones, text="Calcular", 
                  command=self.calcular).pack(side="left")
        
        frame_resultados = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        frame_resultados.grid(row=5, column=0, columnspan=2, sticky="nsew")
        main_frame.rowconfigure(5, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        self.resultados_texto = tk.Text(frame_resultados, height=15, width=70, font=("Consolas", 10))
        self.resultados_texto.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient="vertical", command=self.resultados_texto.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.resultados_texto.configure(yscrollcommand=scrollbar.set)
        
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)

    def cargar_archivo(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo", 
                                              filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if not file_path: return
        try:
            with open(file_path, 'r') as file:
                contenido = file.read().strip()
                self.entrada_datos.delete(0, tk.END)
                self.entrada_datos.insert(0, contenido)
                messagebox.showinfo("Éxito", "Archivo cargado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    def obtener_datos(self):
        texto = self.entrada_datos.get().strip()
        datos = CalculadoraTendenciaCentral.texto_a_lista(texto)
        if not datos: 
            messagebox.showerror("Error", "Ingresa datos válidos (números separados por comas)")
            return None
        return datos

    def calcular(self):
        datos = self.obtener_datos()
        if not datos: return
        
        calc = CalculadoraTendenciaCentral
        media = calc.calcular_media(datos)
        mediana = calc.calcular_mediana(datos)
        moda = calc.calcular_moda(datos)
        desviacion = calc.calcular_desviacion_estandar(datos)
        rango = calc.calcular_rango(datos)
        cuartiles = calc.calcular_cuartiles(datos)
        
        resultado_texto = f"DATOS: {datos}\n\n"
        resultado_texto += f"CANTIDAD: {len(datos)}\n"
        resultado_texto += f"MÍNIMO: {min(datos):.2f}\n"
        resultado_texto += f"MÁXIMO: {max(datos):.2f}\n"
        resultado_texto += f"RANGO: {rango:.2f}\n\n"
        
        resultado_texto += "MEDIDAS DE TENDENCIA CENTRAL:\n"
        resultado_texto += f"Media: {media:.4f}\n"
        resultado_texto += f"Mediana: {mediana:.4f}\n"
        resultado_texto += f"Moda: {', '.join(f'{m:.2f}' for m in moda) if moda else 'No hay moda'}\n\n"
        
        resultado_texto += "MEDIDAS DE DISPERSIÓN:\n"
        resultado_texto += f"Desviación estándar: {desviacion:.4f}\n\n"
        
        resultado_texto += "CUARTILES:\n"
        resultado_texto += f"Q1 (25%): {cuartiles['Q1']:.4f}\n"
        resultado_texto += f"Q2 (50% - Mediana): {cuartiles['Q2']:.4f}\n"
        resultado_texto += f"Q3 (75%): {cuartiles['Q3']:.4f}\n"
        
        self.resultados_texto.delete(1.0, tk.END)
        self.resultados_texto.insert(1.0, resultado_texto)

    def calcular_intervalos(self):
        datos = self.obtener_datos()
        if not datos: return
        
        resultado = CalculadoraTendenciaCentral.calcular_por_intervalos(datos)
        num_intervalos = resultado["num_intervalos"]
        amplitud = resultado["amplitud"]
        
        resultado_texto = f"CÁLCULO POR INTERVALOS \n"
        resultado_texto += f"Número de intervalos: {num_intervalos} \n"
        resultado_texto += f"Amplitud: {amplitud:.2f}\n\n"
        
        resultado_texto += "TABLA DE DISTRIBUCIÓN DE FRECUENCIAS:\n"
        resultado_texto += "Intervalo\t\tMarca\tFrecuencia\tF.Acum\tF.Relativa\n"
        resultado_texto += "-" * 65 + "\n"
        
        for i, ((ini, fin), marca, freq, facum, frel) in enumerate(zip(
            resultado["intervalos"], resultado["marcas_clase"], resultado["frecuencias"],
            resultado["frecuencias_acumuladas"], resultado["frecuencias_relativas"])):
            
            # Formatear el intervalo para mejor visualización
            intervalo_str = f"[{ini:.2f} - {fin:.2f})"
            resultado_texto += f"{intervalo_str}\t\t{marca:.2f}\t{freq}\t{facum}\t{frel:.3f}\n"
        
        resultado_texto += f"\nMedia aproximada por intervalos: {resultado['media_aproximada']:.4f}\n"
        resultado_texto += f"Media real: {CalculadoraTendenciaCentral.calcular_media(datos):.4f}\n"
        
        self.resultados_texto.delete(1.0, tk.END)
        self.resultados_texto.insert(1.0, resultado_texto)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCalculadora(root)
    root.mainloop()