#!/bin/sh

# Créer la base et l'utilisateur

DB_USER_PWD=$(cat /run/secrets/${DB_AUTH_SECRETS})

psql -U postgres << EOF
CREATE DATABASE ${DB_AUTH_NAME};
CREATE USER ${DB_AUTH_USER} WITH PASSWORD '${DB_USER_PWD}';
GRANT ALL PRIVILEGES ON DATABASE ${DB_AUTH_NAME} TO ${DB_AUTH_USER};
EOF

# Donner les droits sur le schema public
psql -U postgres -d ${DB_AUTH_NAME} << EOF
GRANT ALL ON SCHEMA public TO ${DB_AUTH_USER};
EOF

echo "Base de données et table initialisées avec succès !"