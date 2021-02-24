FROM postgres
WORKDIR /backend/psql_docker

RUN get-apt install awk
RUN chmod +x entry-point.sh

CMD ["./entry-point.sh"]

RUN PGOPTIONS="-c 'custom.name=${PSQL_DATABASE_NAME}'"
RUN PGOPTIONS="-c 'custom.user=${PSQL_DATABASE_USER}'"
RUN PGOPTIONS="-c 'custom.password=${PSQL_DATABASE_PASSWORD}'"
RUN PGOPTIONS="-c 'custom.hostname=${PSQL_DATABASE_HOSTNAME}'"
RUN PGOPTIONS="-c 'custom.port=${PSQL_DATABASE_PORT}'"
RUN POSTGRES_PASSWORD='${PSQL_DATABASE_PASSWORD}'
