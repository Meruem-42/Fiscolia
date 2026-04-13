#!/bin/sh

# Créer la base et l'utilisateur
psql -U postgres << EOF
CREATE DATABASE auth;
CREATE USER admin WITH PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE auth TO admin;
ALTER USER postgres WITH PASSWORD '2345';
EOF

# Donner les droits sur le schema public
psql -U postgres -d auth << EOF
GRANT ALL ON SCHEMA public TO admin;
EOF

echo "Base de données et table initialisées avec succès !"