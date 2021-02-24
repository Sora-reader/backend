#!/bin/bash

text="$(echo | awk -f get_env.awk ../manga_reader/config/.env);"
myarray=($text)

export PSQL_DATABASE_NAME="${myarray[1]}"
export PSQL_DATABASE_USER="${myarray[2]}"
export PSQL_DATABASE_PASSWORD="${myarray[3]}"
export PSQL_DATABASE_HOSTNAME="${myarray[4]}"
export PSQL_DATABASE_PORT="${myarray[5]}"
