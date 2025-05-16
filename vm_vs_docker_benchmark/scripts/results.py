import subprocess
import time
import os

RESULTS_DIR = "../results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Archivos fuente por lenguaje
sources = {
    "python": "Sucesionfibonacci.py",
    "java": "Sucesionfibonacci.java",
    "javascript": "Sucesionfibonacci.js"
}

# Comandos de ejecución por lenguaje
commands = {
    "python": ["python", sources["python"]],
    "java": ["java", "Sucesionfibonacci"],
    "javascript": ["node", sources["javascript"]]
}

def compilar_java():
    try:
        subprocess.run(["javac", sources["java"]], check=True)
        print("Compilación de Java completada con éxito")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al compilar Java: {e}")
        return False
    except FileNotFoundError:
        print("Archivo Java no encontrado.")
        return False

def medir_tiempo(comando):
    start = time.perf_counter()
    try:
        output = subprocess.check_output(comando, stderr=subprocess.STDOUT, text=True, input="100\n")
        error = None
    except subprocess.CalledProcessError as e:
        output = e.output
        error = str(e)
    end = time.perf_counter()
    tiempo = end - start
    return tiempo, output, error

def guardar_resultados(idioma, tiempo, output, error):
    nombre_archivo = os.path.join(RESULTS_DIR, f"resultado_{idioma}.txt")
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"Tiempo de ejecución: {tiempo:.6f} segundos\n\n")
        f.write("Salida del programa:\n")
        f.write(output)
        if error:
            f.write("\n\nErrores:\n")
            f.write(error)

def main():
    java_compilado = compilar_java()

    for idioma in commands:
        if not os.path.exists(sources[idioma]):
            print(f"Archivo fuente de {idioma} no encontrado, saltando...")
            continue

        if idioma == "java" and not java_compilado:
            print("Saltando ejecución de Java debido a errores de compilación")
            continue

        print(f"Ejecutando {idioma}...")
        tiempo, output, error = medir_tiempo(commands[idioma])
        guardar_resultados(idioma, tiempo, output, error)
        print(f"Terminado {idioma}: {tiempo:.6f} segundos")

if __name__ == "__main__":
    main()
