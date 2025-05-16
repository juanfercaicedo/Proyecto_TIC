FROM python:3.12-slim

# Instala dependencias necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instala Node.js 
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Establece directorio de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY Sucesionfibonacci.py /app/Sucesionfibonacci.py
COPY Sucesionfibonacci.js /app/Sucesionfibonacci.js
COPY Sucesionfibonacci.java /app/Sucesionfibonacci.java

# Instala paquetes de Python si los necesitas
RUN pip install --no-cache-dir \
    numpy \
    matplotlib

# Compila el archivo Java
RUN javac Sucesionfibonacci.java

# Comando por defecto (puedes elegir cuál ejecutar)
CMD ["python", "Sucesionfibonacci.py"]