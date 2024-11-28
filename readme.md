# Redis Data Processor

Este proyecto implementa un sistema simple y escalable para procesar mensajes en paralelo utilizando Redis Streams, gestionado por Prometheus y Grafana. Es ideal como ejemplo de un sistema distribuido tipo "hola mundo" que gestiona colas de mensajes, los procesa en paralelo y almacena los resultados en una base de datos SQL Server.

## Propósito

El propósito de este proyecto es crear un **paralelizador de procesamiento** gestionado con colas en Redis. La API gestiona los mensajes de entrada, que luego son procesados en paralelo por múltiples contenedores y almacenados en una base de datos. Además, incluye un **dashboard** simple que utiliza Prometheus y Grafana para monitorear las métricas clave del sistema.

---

## Arquitectura

El proyecto incluye los siguientes servicios:

1. **Redis**: Servidor de colas con Streams habilitado.
2. **Redis Exporter**: Exporta métricas de Redis para Prometheus.
3. **Prometheus**: Sistema de monitoreo que recopila métricas de Redis Exporter.
4. **Grafana**: Interfaz visual para monitorear métricas con Prometheus.
5. **FastAPI**: API que envía mensajes a las colas de Redis.
6. **Processor**: Microservicio que procesa mensajes en paralelo desde Redis Streams.
7. **Writer**: Microservicio que escribe los resultados procesados en una base de datos SQL Server.
8. **SQL Server**: Base de datos donde se almacenan los datos procesados.

---

## Configuración del proyecto

### Archivos clave:

1. **`docker-compose.yml`**: Define la configuración de los servicios en contenedores.
2. **`prometheus.yml`**: Configuración para Prometheus, especificando los endpoints de Redis Exporter.
3. **`processor/config.py`**: Configuración específica del Processor, como el nombre de la cola y los tiempos de espera.
4. **`writer/config.py`**: Configuración del Writer, incluyendo la URL de conexión a la base de datos.
5. **`brqm.py`**: Librería reutilizable para manejar Redis Streams.
6. **`processor/main.py`** y **`writer/main.py`**: Lógica principal de cada servicio.

---

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <url-del-repo>
   cd RedisDataProcessor
   ```

2. Construye y levanta los contenedores:
   ```bash
   docker-compose up --build -d
   ```

3. Crea la base de datos `yourdb` en SQL Server:
   ```bash
   docker exec -it sqlserver /opt/mssql-tools/bin/sqlcmd -S sqlserver -U SA -P "YourPassword123" -Q "CREATE DATABASE yourdb;"
   ```

---

## Cómo funciona

1. **API (FastAPI)**:
   - Recibe solicitudes HTTP para insertar mensajes en `queue_a` (cola de entrada).

2. **Processor**:
   - Lee mensajes desde `queue_a`.
   - Procesa el mensaje usando la librería `processor_lib`.
   - Publica los resultados en `queue_b`.
   - Mantiene métricas como `processed_messages` y `rejected_messages`.

3. **Writer**:
   - Lee mensajes desde `queue_b`.
   - Escribe los resultados en la base de datos `yourdb`.

4. **Dashboard**:
   - Prometheus recopila métricas de Redis Exporter.
   - Grafana visualiza métricas como:
     - Número de mensajes procesados.
     - Longitud de las colas.

---

## Métricas clave

El sistema utiliza métricas específicas que son visibles en el dashboard de Grafana:

- **Mensajes procesados**: `queue_a:processed_messages`
- **Mensajes rechazados**: `queue_a:rejected_messages`
- **Longitud de las colas**:
  - `queue_a`
  - `queue_b`
- **Tiempo de inactividad del consumidor**: Métrica basada en Redis Streams.

---

## Uso de Prometheus y Grafana

1. Accede a **Prometheus**:
   - URL: [http://localhost:9090](http://localhost:9090)

2. Accede a **Grafana**:
   - URL: [http://localhost:3000](http://localhost:3000)
   - Credenciales por defecto:
     - Usuario: `admin`
     - Contraseña: `admin`

3. Importa el dashboard de Grafana:
   - Usa el ID proporcionado o crea tu propio dashboard configurando las métricas.

---

## Ejemplo de procesamiento

1. **Entrada**: La API inserta un mensaje en `queue_a`:
   ```json
   {"query": "procesar este mensaje"}
   ```

2. **Proceso**:
   - `Processor` lee el mensaje desde `queue_a`.
   - Procesa el mensaje.
   - Inserta el resultado en `queue_b`.

3. **Salida**:
   - `Writer` lee el mensaje desde `queue_b`.
   - Inserta el resultado en la base de datos `yourdb`.

---

## Escalabilidad

- **Processor**: Escalable mediante réplicas en `docker-compose.yml`:
  ```yaml
  deploy:
    replicas: 4
  ```

- **Prometheus y Grafana**:
  - Monitorea múltiples instancias del Processor y Writer.

---

## Notas importantes

- **Volúmenes persistentes**:
  - Redis: `redis_data`
  - SQL Server: `sqlserver_data`
  - Grafana: `grafana_data`

- **Creación de base de datos**:
  - Asegúrate de crear la base de datos `yourdb` antes de iniciar el sistema. Sin esto el contenedor `writer` no va a funcionar. En caso de que pase, simplemente accede al contenedor de sqlserver y crea la base.
  ```bash
  /opt/mssql-tools/bin/sqlcmd -S sqlserver -U SA -P "YourPassword123" -Q "CREATE DATABASE yourdb;"
  ```

- **Configuraciones**:
  - Actualiza las contraseñas y nombres de las colas si es necesario en los archivos `config.py`.





