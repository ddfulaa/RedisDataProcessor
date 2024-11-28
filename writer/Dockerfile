# Usa una imagen ligera de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para SQL Server
# Instala dependencias necesarias para SQL Server y maneja conflictos
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    gnupg \
    unixodbc \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && apt-get remove -y libodbc2 unixodbc-common \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Copia el archivo Pipfile y Pipfile.lock
COPY Pipfile /app/

# Instala pipenv y las dependencias del proyecto
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy

# Copia el resto de los archivos de la aplicación
COPY . /app

# Comando para ejecutar el escritor
CMD ["pipenv", "run", "python", "main.py"]
