# Usar una imagen base de Python
FROM python:3.9-slim

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto a la imagen Docker
COPY . .

# Instalar las dependencias de la aplicación
RUN pip install -r requirements.txt

# Exponer el puerto en el que correrá Flask
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "main.py"]
