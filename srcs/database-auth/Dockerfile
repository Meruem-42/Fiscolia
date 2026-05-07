FROM docker.io/library/postgres:15-alpine

COPY ./init.sh /docker-entrypoint-initdb.d

ARG DB_AUTH_PORT
EXPOSE $DB_AUTH_PORT
