#!/bin/sh
echo ${ls -a}
text="$(echo | awk -f get_env.awk ../manga_reader/config/.env);"
myarray=($text)

export PSQL_DATABASE_NAME="${myarray[1]}"
export PSQL_DATABASE_USER="${myarray[2]}"
export PSQL_DATABASE_PASSWORD="${myarray[3]}"
export PSQL_DATABASE_HOSTNAME="${myarray[4]}"
export PSQL_DATABASE_PORT="${myarray[5]}"
set -e

psql -c ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" "
    CREATE USER $PSQL_DATABASE_USER WITH PASSWORD $PSQL_DATABASE_PASSWORD;
    CREATE DATABASE $PSQL_DATABASE_NAME;
    GRANT ALL PRIVILEGES ON DATABASE $PSQL_DATABASE_NAME TO $PSQL_DATABASE_USER;
"