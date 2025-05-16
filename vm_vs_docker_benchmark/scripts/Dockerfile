FROM python:3.12-slim

# Instala dependencias necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    build-essential \
    python3-dev \
    curl \
    git \
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
COPY Sucesionfibonacci.cpp /app/Sucesionfibonacci.cpp


# Instala paquetes de Python
RUN pip install --no-cache-dir \
    numpy \
    matplotlib

# Compila el archivo C++
RUN g++ Sucesionfibonacci.cpp -o sucesion_cpp

# Comando por defecto
CMD ["python", "Sucesionfibonacci.py"]
