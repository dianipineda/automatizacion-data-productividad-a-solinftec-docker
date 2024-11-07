FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    cron \
    libaio1 \
    wget \
    unzip 

COPY instantclient-basic-linux.x64-19.23.0.0.0dbru.zip /tmp/instantclient.zip

RUN unzip /tmp/instantclient.zip -d /opt/oracle/ && \
    rm /tmp/instantclient.zip

ENV ORACLE_HOME=/opt/oracle/instantclient_19_23
ENV LD_LIBRARY_PATH=$ORACLE_HOME:$LD_LIBRARY_PATH
ENV PATH=$ORACLE_HOME:$PATH
ENV TNS_ADMIN=$ORACLE_HOME

COPY requeriments.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requeriments.txt
COPY . /app/
# Crear el cron job
# En este caso, el cron job ejecutará `python main.py` cada 3 minutos
RUN echo "*/3 * * * * python /app/main.py" >> /etc/cron.d/mycron

# Cambiar los permisos del archivo cron
RUN chmod 0644 /etc/cron.d/mycron

# Aplicar el cron job
RUN crontab /etc/cron.d/mycron

# Crear el directorio para los logs de cron
RUN touch /var/log/cron.log

# Iniciar el servicio de cron en segundo plano y el contenedor
CMD cron && tail -f /var/log/cron.log
