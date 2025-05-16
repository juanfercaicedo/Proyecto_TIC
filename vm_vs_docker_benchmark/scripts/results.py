import subprocess
import time
import os

# Carpeta donde guardar resultados
RESULTS_DIR = "../results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Comandos para ejecutar los programas (ajusta según cómo los corras)
commands = {
    "python": ["python3", "Sucesionfibonacci.py"],
    "cpp": ["./Sucesionfibonacci_CPP/sucesion_cpp"],
    "javascript": ["node", "Sucesionfibonacci.js"]
}

def medir_tiempo(comando):
    start = time.perf_counter()
    try:
        output = subprocess.check_output(comando, stderr=subprocess.STDOUT, text=True)
        error = None
    except subprocess.CalledProcessError as e:
        output = e.output
        error = str(e)
    end = time.perf_counter()
    tiempo = end - start
    return tiempo, output, error

def guardar_resultados(idioma, tiempo, output, error):
    nombre_archivo = os.path.join(RESULTS_DIR, f"resultado_{idioma}.txt")
    with open(nombre_archivo, "w") as f:
        f.write(f"Tiempo de ejecución: {tiempo:.6f} segundos\n\n")
        f.write("Salida del programa:\n")
        f.write(output)
        if error:
            f.write("\n\nErrores:\n")
            f.write(error)

def main():
    for idioma, comando in commands.items():
        print(f"Ejecutando {idioma}...")
        tiempo, output, error = medir_tiempo(comando)
        guardar_resultados(idioma, tiempo, output, error)
        print(f"Terminado {idioma}: {tiempo:.6f} segundos")

if __name__ == "__main__":
    main()
