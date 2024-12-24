FROM python:3.10.11

WORKDIR /app
COPY requeriments.txt /app/

#? comentar/descomentar modo escritorio
# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    cron \ 
    libaio1 \
    wget \
    unzip \
    procps && \
    rm -rf /var/lib/apt/lists/*

#? comentar/descomentar modo web
# RUN apt-get update && apt-get install -y unzip procps
# RUN rm -rf /var/lib/apt/lists/*

# COPY instantclient-basic-linux.x64-19.23.0.0.0dbru.zip /tmp/instantclient.zip

# RUN unzip /tmp/instantclient.zip -d /opt/oracle/ && \
#     rm /tmp/instantclient.zip
    
# Crear el entorno virtual
RUN python -m venv /app/venv

# Actualizar pip
RUN /app/venv/bin/pip install --upgrade pip

# Copiar el archivo requeriments.txt
COPY requeriments.txt /app/

# Instalar las dependencias
RUN /app/venv/bin/pip install -r /app/requeriments.txt

COPY . /app/

# Configurar variables de entorno de Oracle
ENV ORACLE_HOME=/opt/oracle/instantclient_19_23
ENV LD_LIBRARY_PATH=$ORACLE_HOME:$LD_LIBRARY_PATH
ENV PATH=$ORACLE_HOME:$PATH
ENV TNS_ADMIN=$ORACLE_HOME


# Crear y configurar el cron job con las variables de entorno cargadas
#comentar/descomentar - prod
#?RUN echo "15 6 * * 1-6 . /etc/environment; export LD_LIBRARY_PATH=$ORACLE_HOME && /app/venv/bin/python /app/main.py >> /var/log/myapp.log 2>&1" > /etc/cron.d/mycron
#comentar/descomentar - dev
#?RUN echo "*/3 * * * * . /etc/environment; export LD_LIBRARY_PATH=$ORACLE_HOME && /app/venv/bin/python /app/main.py >> /var/log/myapp.log 2>&1" > /etc/cron.d/mycron


#?RUN chmod 0644 /etc/cron.d/mycron
#?RUN crontab /etc/cron.d/mycron

# Asegurar permisos de los logs
#?RUN touch /var/log/myapp.log && chmod 666 /var/log/myapp.log

# Iniciar cron en segundo plano y seguir el archivo de log
#?CMD ["cron", "-f"]

#!Nota:
    #?comentar/descomentar para desactivar/activar la funcionalidad de tarea programada de esta app