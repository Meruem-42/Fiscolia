#!/bin/sh
set -e

vault server -dev \
    -dev-listen-address=${VAULT_DEV_LISTEN_ADDRESS} \
    -dev-root-token-id="${VAULT_DEV_ROOT_TOKEN_ID}" &

sleep 3
export VAULT_ADDR=${VAULT_ADDR}
export VAULT_TOKEN=${VAULT_DEV_ROOT_TOKEN_ID}

vault status
vault secrets enable -version=2 -path=legacy-secrets kv

vault kv put secret/database \
    project_name=${PROJECT_NAME} \
    db_user=${DB_AUTH_USER} \
    db_password=@/run/secrets/db_auth_pwd \
    db_port=${DB_AUTH_PORT} \
    db_name=${DB_AUTH_NAME} \
    postres_password=@/run/secrets/db_root_pwd \
    backend_port=${BACK_AUTH_PORT}  \
    upload_port=${BACK_UPLOAD_PORT} \
    front_port=${FRONT_PORT}    \
    proxy_port=${PROXY_EXPOSED_PORT}    \




#vault kv put -mount=secret PROJECT_NAME=${PROJECT_NAME}

wait