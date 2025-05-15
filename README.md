# 🧪 Proyecto TIC: Comparativa de Rendimiento y Experiencia de Desarrollo

## 🐳 Docker vs 🖥️ VM vs 🧑‍💻 Host

---

## 🎯 Objetivo

Comparar el rendimiento y la experiencia al desarrollar y ejecutar aplicaciones sencillas en distintos entornos:

- Máquina virtual (Ubuntu en VirtualBox)
- Contenedor Docker
- Sistema operativo anfitrión (host)

---

## 📏 Métricas Cuantitativas

### ⏱️ Tiempo de ejecución de scripts

- **Lenguajes**: Python, JavaScript, C++
- **Herramientas de medición**: `time`, `hyperfine`
- **Scripts sugeridos**:
  - Cálculo de Fibonacci
  - Algoritmo de ordenamiento (ej. quicksort)
  - Lectura y procesamiento de archivos

### 🧠 Uso de recursos del sistema

- **CPU y RAM** durante la ejecución:
  - Herramientas: `htop`, `docker stats`, `vmstat`

### 💾 Tamaño del entorno

- Docker: peso de la imagen (`docker image ls`)
- VM: tamaño del disco de la máquina virtual
- Host: uso de disco adicional requerido por dependencias

### 🚀 Tiempo de inicio del entorno

- ¿Cuánto tarda en estar listo para ejecutar un script?
  - Docker: desde `docker run`
  - VM: desde arranque hasta login y terminal disponible

---

## 📋 Evaluación Cualitativa

### ⚙️ Facilidad de configuración

- ¿Qué tan fácil es instalar dependencias y preparar el entorno?

### ✍️ Experiencia de desarrollo

- Uso de editores de texto: `VS Code`, `nano`
- Facilidad para escribir, guardar y ejecutar código

### 🔁 Portabilidad del proyecto

- ¿Es fácil mover o replicar el proyecto en otra máquina?

---

## 🧰 Herramientas Necesarias

| Categoría | Herramientas                                          |
| --------- | ----------------------------------------------------- |
| Lenguajes | Python, JavaScript , C++                              |
| Entornos  | Docker, VirtualBox (Ubuntu), Host                     |
| Medición  | `time`, `hyperfine`, `htop`, `vmstat`, `docker stats` |
| Edición   | VS Code, nano                                         |

---

## ✅ Resultados Esperados

- Comparativas claras de rendimiento entre entornos
- Tabla resumen de tiempos y recursos
- Conclusiones sobre cuál entorno es más eficiente, fácil de usar y portable
