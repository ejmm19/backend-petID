# Usamos la imagen oficial de Python
FROM python:3.11

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos al contenedor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos la aplicación al contenedor
COPY app /app/app

# Exponemos el puerto 8000
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
