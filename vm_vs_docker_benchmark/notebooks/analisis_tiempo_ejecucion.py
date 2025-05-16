"""
Análisis Comparativo de Tiempos de Ejecución: Docker vs VM

Este script analiza y compara los tiempos de ejecución entre entornos Docker y VM,
cargando datos desde las carpetas 'results-docker' y 'results-vm'.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob

def main():
    """Función principal que ejecuta todo el análisis"""
    print("Iniciando análisis comparativo de tiempos de ejecución entre Docker y VM...")
    
    # Asegurar que existan los directorios necesarios
    check_directories()
    
    # Configurar estilo de las gráficas
    plt.style.use('ggplot')
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 7)
    plt.rcParams['font.size'] = 12
    
    # Definir rutas a los archivos de resultados
    docker_results_path = "./results-docker/"
    vm_results_path = "./results-vm/"
    
    # Cargar datos
    print("\n" + "="*70)
    print("CARGANDO DATOS DE DOCKER")
    print("="*70)
    docker_data = load_execution_times(docker_results_path)
    print(f"Se cargaron {len(docker_data)} registros de Docker")
    
    print("\n" + "="*70)
    print("CARGANDO DATOS DE VM")
    print("="*70)
    vm_data = load_execution_times(vm_results_path)
    print(f"Se cargaron {len(vm_data)} registros de VM")
    print("="*70 + "\n")
    
    # Agregar columna para identificar el entorno
    if not docker_data.empty:
        docker_data['environment'] = 'Docker'
    else:
        print("ADVERTENCIA: No se encontraron datos válidos para Docker.")
    
    if not vm_data.empty:
        vm_data['environment'] = 'VM'
    else:
        print("ADVERTENCIA: No se encontraron datos válidos para VM.")
    
    # Combinar datos
    all_data = pd.concat([docker_data, vm_data], ignore_index=True)
    
    # Verificar si tenemos datos para procesar
    if all_data.empty:
        print("\nNo hay datos para analizar. Por favor, asegúrese de que existan archivos TXT válidos en las carpetas 'results-docker' y 'results-vm'.")
        print("\nPuede intentar agregar manualmente algunos archivos de resultados para realizar el análisis.")
        print("Ejemplo de formato de archivo de resultados:")
        print("---")
        print("Tiempo de ejecución: 2.5 segundos")
        print("---")
        return
    
    # Eliminar filas con valores NaN si existen
    if 'execution_time' in all_data.columns and all_data['execution_time'].isna().any():
        na_count = all_data['execution_time'].isna().sum()
        print(f"\nEliminando {na_count} filas con valores de tiempo no válidos.")
        all_data = all_data.dropna(subset=['execution_time'])
    
    # Mostrar datos cargados
    if not all_data.empty:
        print("\nDatos cargados:")
        print(all_data)
    
    # Verificar nuevamente si tenemos datos suficientes después de eliminar NaN
    if all_data.empty or len(all_data) < 2:
        print("\nNo hay suficientes datos para realizar un análisis comparativo. Se necesitan al menos dos registros (uno de Docker y uno de VM).")
        return
    
    # Verificar si tenemos datos de ambos entornos
    if 'Docker' not in all_data['environment'].values:
        print("\nNo hay datos válidos para Docker. No se puede realizar comparación.")
        return
    if 'VM' not in all_data['environment'].values:
        print("\nNo hay datos válidos para VM. No se puede realizar comparación.")
        return
    
    # Realizar análisis estadístico
    perform_statistical_analysis(all_data)
    
    # Crear visualizaciones
    create_visualizations(all_data)
    
    # Generar conclusiones
    
    print("\nAnálisis completado. Las gráficas se han guardado en el directorio principal.")


def check_directories():
    """Verifica que existan los directorios necesarios y los crea si no existen"""
    # Verificar directorio padre
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Verificar directorios de resultados
    docker_dir = os.path.join(parent_dir, "results-docker")
    vm_dir = os.path.join(parent_dir, "results-vm")
    
    for dir_path in [docker_dir, vm_dir]:
        if not os.path.exists(dir_path):
            print(f"Creando directorio: {dir_path}")
            os.makedirs(dir_path)
            print(f"ADVERTENCIA: El directorio {os.path.basename(dir_path)} no existía y ha sido creado.")
            print(f"Por favor, coloque los archivos de resultados en {dir_path} antes de ejecutar este script.")
    
    return True


def load_execution_times(directory):
    """Carga los tiempos de ejecución desde archivos TXT en el directorio especificado"""
    all_files = glob.glob(os.path.join(directory, "*.txt"))
    
    if not all_files:
        print(f"No se encontraron archivos TXT en {directory}")
        return pd.DataFrame(columns=['file', 'execution_time'])  # Devolver DataFrame vacío pero con columnas
    
    data = []
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                print(f"Procesando archivo: {os.path.basename(file_path)}")
                
                # Imprimir primeras líneas para depuración
                print(f"Primeras 3 líneas del archivo:")
                content_lines = content.split('\n')
                for i, line in enumerate(content_lines[:3]):
                    print(f"  Línea {i+1}: {line}")
                
                # Buscar tiempos de ejecución
                time_values = []
                
                # Método principal: Buscar específicamente el patrón "Tiempo de ejecución: X segundos"
                # Este patrón parece ser el más común en tus archivos
                import re
                tiempo_pattern = re.compile(r'Tiempo de ejecuci[óo]n:\s*(\d+\.\d+)\s*segundos', re.IGNORECASE)
                
                # Primero, revisar las primeras líneas para el patrón de tiempo
                for line in content_lines[:10]:  # Revisar primeras 10 líneas
                    match = tiempo_pattern.search(line)
                    if match:
                        try:
                            value = float(match.group(1))
                            print(f"  Encontrado tiempo de ejecución: {value} segundos")
                            time_values.append(value)
                            break  # Encontramos el tiempo principal, no necesitamos buscar más
                        except ValueError:
                            pass
                
                # Si no encontramos el patrón específico, intentar con una búsqueda más generalizada
                if not time_values:
                    # Método 1: Buscar valores numéricos en líneas que contengan palabras clave
                    for line in content_lines:
                        # Palabras clave que podrían indicar un tiempo de ejecución
                        if any(keyword in line.lower() for keyword in ['tiempo', 'time', 'duration', 'execution', 'seg', 'sec', 'segundos', 'seconds']):
                            try:
                                # Intentar extraer números de la línea
                                numbers = []
                                for word in line.split():
                                    word = word.strip()
                                    # Limpiar la palabra de caracteres no numéricos al principio/final
                                    clean_word = word.strip(',:;()[]{}"\'' + "'")
                                    # Verificar si es un número con posible punto decimal
                                    if clean_word.replace('.', '', 1).isdigit():
                                        numbers.append(float(clean_word))
                                
                                if numbers:
                                    print(f"  Encontrado posible tiempo: {numbers[0]} en la línea: {line}")
                                    time_values.append(numbers[0])
                            except Exception as e:
                                print(f"  Error al extraer número de la línea: {line}, Error: {e}")
                    
                    # Método 2: Si no se encontraron valores, intentar buscar números al final del archivo
                    if not time_values:
                        print("  No se encontraron valores usando palabras clave, buscando números solitarios...")
                        lines = content.strip().split('\n')
                        # Revisar las últimas líneas del archivo
                        for line in lines[-5:]:  # Revisar últimas 5 líneas
                            line = line.strip()
                            if line and all(c.isdigit() or c in '.,+-' for c in line):
                                try:
                                    value = float(line.replace(',', '.'))
                                    print(f"  Encontrado valor numérico: {value}")
                                    time_values.append(value)
                                except ValueError:
                                    pass
                    
                    # Método 3: Buscar patrones específicos como "X segundos" o "X s"
                    if not time_values:
                        print("  Buscando patrones específicos de tiempo...")
                        # Patrones como "10 segundos", "10s", "10 s", etc.
                        patterns = [
                            r'(\d+\.?\d*)\s*segundos',
                            r'(\d+\.?\d*)\s*s\b',
                            r'(\d+\.?\d*)\s*sec',
                            r'tiempo:?\s*(\d+\.?\d*)',
                            r'time:?\s*(\d+\.?\d*)'
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, content.lower())
                            if matches:
                                for match in matches:
                                    try:
                                        value = float(match)
                                        print(f"  Encontrado con patrón: {value}")
                                        time_values.append(value)
                                    except ValueError:
                                        continue
                
                # Si encontramos valores de tiempo
                if time_values:
                    # Usar la mediana para evitar outliers extremos si hay múltiples valores
                    # o el primer valor si solo hay uno
                    exec_time = time_values[0] if len(time_values) == 1 else np.median(time_values)
                    print(f"  Tiempo calculado para {os.path.basename(file_path)}: {exec_time}")
                    data.append({
                        'file': os.path.basename(file_path),
                        'execution_time': exec_time
                    })
                else:
                    print(f"  ADVERTENCIA: No se encontraron valores de tiempo en {file_path}")
                    # Agregar un marcador para que el archivo aparezca en el análisis
                    # con un valor de tiempo ficticio (NaN)
                    data.append({
                        'file': os.path.basename(file_path),
                        'execution_time': np.nan
                    })
                
                print("-" * 50)
        except Exception as e:
            print(f"Error al procesar {file_path}: {e}")
    
    result_df = pd.DataFrame(data)
    
    # Si hay valores NaN, informarlo
    if 'execution_time' in result_df.columns and result_df['execution_time'].isna().any():
        print("Nota: Algunos archivos no tenían valores de tiempo detectables.")
    
    return result_df


def load_csv_data(directory):
    """Función alternativa para cargar datos desde CSVs"""
    all_files = glob.glob(os.path.join(directory, "*.csv"))
    
    if not all_files:
        print(f"No se encontraron archivos CSV en {directory}")
        return pd.DataFrame()
    
    dfs = []
    for file_path in all_files:
        try:
            df = pd.read_csv(file_path)
            df['file'] = os.path.basename(file_path)
            dfs.append(df)
        except Exception as e:
            print(f"Error al leer {file_path}: {e}")
    
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()


def perform_statistical_analysis(all_data):
    """Realiza análisis estadístico básico de los datos"""
    # Estadísticas descriptivas por entorno
    stats = all_data.groupby('environment')['execution_time'].describe()
    print("\nEstadísticas de tiempo de ejecución por entorno:")
    print(stats)
    
    # Calcular la diferencia porcentual entre Docker y VM
    if 'Docker' in all_data['environment'].values and 'VM' in all_data['environment'].values:
        docker_mean = all_data[all_data['environment'] == 'Docker']['execution_time'].mean()
        vm_mean = all_data[all_data['environment'] == 'VM']['execution_time'].mean()
        
        if vm_mean > 0:  # Evitar división por cero
            percent_diff = ((docker_mean - vm_mean) / vm_mean) * 100
            faster = "Docker" if docker_mean < vm_mean else "VM"
            print(f"\nDiferencia porcentual: {abs(percent_diff):.2f}% ({faster} es más rápido)")
            
            # Mostrar tiempo promedio
            print(f"\nTiempo promedio en Docker: {docker_mean:.4f} segundos")
            print(f"Tiempo promedio en VM: {vm_mean:.4f} segundos")


def create_visualizations(all_data):
    """Crea visualizaciones a partir de los datos"""
    print("\nGenerando visualizaciones...")
    output_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Comparación directa con gráfico de barras
    print("- Creando gráfico de barras comparativo...")
    plt.figure(figsize=(10, 6))
    
    # Gráfico de barras para comparar tiempos promedio
    avg_times = all_data.groupby('environment')['execution_time'].mean()
    
    ax = avg_times.plot(kind='bar', color=['#3498db', '#e74c3c'])
    plt.title('Comparación de Tiempo de Ejecución Promedio: Docker vs VM', fontsize=16)
    plt.xlabel('Entorno', fontsize=14)
    plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Agregar valores en las barras
    for i, value in enumerate(avg_times):
        plt.text(i, value + (value*0.05), f'{value:.3f}s', ha='center', fontweight='bold')
    
    plt.tight_layout()
    bar_chart_path = os.path.join(output_dir, 'comparison_bar_chart.png')
    plt.savefig(bar_chart_path, dpi=300, bbox_inches='tight')
    print(f"  Gráfico guardado como: {bar_chart_path}")
    
    # 2. Gráfico de caja (Box Plot) para ver la distribución
    if len(all_data) >= 4:  # Se necesitan suficientes puntos para un boxplot útil
        print("- Creando box plot para distribución...")
        plt.figure(figsize=(10, 6))
        
        # Box plot para visualizar la distribución
        sns.boxplot(x='environment', y='execution_time', data=all_data, palette=['#3498db', '#e74c3c'])
        
        # Añadir puntos individuales
        sns.stripplot(x='environment', y='execution_time', data=all_data, color='black', alpha=0.5, size=6)
        
        plt.title('Distribución de Tiempos de Ejecución: Docker vs VM', fontsize=16)
        plt.xlabel('Entorno', fontsize=14)
        plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=14)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        boxplot_path = os.path.join(output_dir, 'comparison_boxplot.png')
        plt.savefig(boxplot_path, dpi=300, bbox_inches='tight')
        print(f"  Gráfico guardado como: {boxplot_path}")
    else:
        print("  Omitiendo box plot: se necesitan más puntos de datos para un box plot útil")
    
    # 3. Histograma de tiempos de ejecución (solo si hay suficientes puntos)
    if len(all_data) >= 6:  # Se necesitan suficientes puntos para un histograma útil
        print("- Creando histograma de tiempos...")
        plt.figure(figsize=(12, 7))
        
        # Crear histograma para cada entorno
        for env, color in zip(['Docker', 'VM'], ['#3498db', '#e74c3c']):
            subset = all_data[all_data['environment'] == env]
            if not subset.empty and len(subset) >= 3:
                sns.histplot(subset['execution_time'], kde=True, label=env, color=color, alpha=0.6)
        
        plt.title('Distribución de Tiempos de Ejecución: Docker vs VM', fontsize=16)
        plt.xlabel('Tiempo de Ejecución (segundos)', fontsize=14)
        plt.ylabel('Frecuencia', fontsize=14)
        plt.grid(linestyle='--', alpha=0.7)
        plt.legend()
        
        plt.tight_layout()
        histogram_path = os.path.join(output_dir, 'comparison_histogram.png')
        plt.savefig(histogram_path, dpi=300, bbox_inches='tight')
        print(f"  Gráfico guardado como: {histogram_path}")
    else:
        print("  Omitiendo histograma: se necesitan más puntos de datos para un histograma útil")
    
    # 4. Gráfico de barras con error (si hay suficientes puntos)
    if all_data.groupby('environment').size().min() >= 2:
        print("- Creando gráfico de barras con barras de error...")
        plt.figure(figsize=(10, 6))
        
        # Calcular medias y errores estándar
        means = all_data.groupby('environment')['execution_time'].mean()
        errors = all_data.groupby('environment')['execution_time'].sem()
        
        # Crear gráfico de barras con barras de error
        ax = means.plot(kind='bar', yerr=errors, capsize=10, color=['#3498db', '#e74c3c'], 
                       error_kw={'elinewidth': 2, 'capthick': 2})
        
        plt.title('Tiempo de Ejecución Promedio con Error Estándar: Docker vs VM', fontsize=16)
        plt.xlabel('Entorno', fontsize=14)
        plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=14)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Agregar valores en las barras
        for i, value in enumerate(means):
            plt.text(i, value + errors[i] + (value*0.05), f'{value:.3f}s', ha='center', fontweight='bold')
        
        plt.tight_layout()
        error_bars_path = os.path.join(output_dir, 'comparison_error_bars.png')
        plt.savefig(error_bars_path, dpi=300, bbox_inches='tight')
        print(f"  Gráfico guardado como: {error_bars_path}")
    else:
        print("  Omitiendo gráfico de barras de error: se necesitan más puntos de datos")
    
    # 5. Gráfico de barras agrupadas por archivo
    if len(all_data['file'].unique()) > 1:
        print("- Creando gráfico comparativo por archivo...")
        
        # Comprobar que hay suficientes datos para pivotar
        pivot_possible = True
        for env in ['Docker', 'VM']:
            for file in all_data['file'].unique():
                if len(all_data[(all_data['environment'] == env) & (all_data['file'] == file)]) == 0:
                    pivot_possible = False
        
        if pivot_possible:
            plt.figure(figsize=(14, 8))
            
            # Preparar datos para gráfico
            pivoted_data = all_data.pivot_table(index='file', columns='environment', values='execution_time', aggfunc='mean')
            
            # Crear gráfico de barras agrupadas
            ax = pivoted_data.plot(kind='bar', figsize=(14, 8))
            
            plt.title('Comparación de Tiempos por Archivo: Docker vs VM', fontsize=16)
            plt.xlabel('Archivo', fontsize=14)
            plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=14)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.legend(title='Entorno')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            by_file_path = os.path.join(output_dir, 'comparison_by_file.png')
            plt.savefig(by_file_path, dpi=300, bbox_inches='tight')
            print(f"  Gráfico guardado como: {by_file_path}")
        else:
            print("  Omitiendo gráfico por archivo: no hay datos para todos los archivos en ambos entornos")
    else:
        print("  Omitiendo gráfico por archivo: solo hay un archivo")
if __name__ == "__main__":
    main()