# Usar una imagen oficial de PostgreSQL
FROM postgres:latest

# Establecer variables de entorno
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=123456789
ENV POSTGRES_DB=mydatabase

# Copiar el script de inicialización de la base de datos
COPY init.sql /docker-entrypoint-initdb.d/
