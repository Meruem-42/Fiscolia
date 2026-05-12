#!/bin/sh
# entrypoint.sh

set -e

export VAULT_ADDR="http://127.0.0.1:8200"
KEYS_FILE="/vault/data/init-keys.json"

vault server -config=/vault/config/vault.hcl &
VAULT_PID=$!

echo "==> Waiting for Vault to respond..."
until vault status 2>/dev/null | grep -q "Initialized"; do
  sleep 1
done

INITIALIZED=$(vault status 2>/dev/null | grep "^Initialized" | awk '{print $2}')

if [ "$INITIALIZED" = "false" ]; then
  echo "==> First start: initializing Vault..."
  vault operator init \
    -key-shares=1 \
    -key-threshold=1 \
    -format=json > "$KEYS_FILE"
  echo "==> Vault initialized."
fi

echo "==> Unsealing Vault..."
# awk читає рядок з hex ключем і витягує значення між лапками
UNSEAL_KEY=$(awk -F'"' '/"unseal_keys_hex"/{getline; print $2}' "$KEYS_FILE")
ROOT_TOKEN=$(awk -F'"' '/"root_token"/{print $4}' "$KEYS_FILE")

echo "DEBUG unseal: $UNSEAL_KEY"
echo "DEBUG token: $ROOT_TOKEN"

vault operator unseal "$UNSEAL_KEY"

echo "$ROOT_TOKEN" > /vault/data/root-token
vault login "$ROOT_TOKEN" > /dev/null

SECRETS_EXIST=$(vault kv get secret/database > /dev/null 2>&1 && echo "yes" || echo "no")

if [ "$SECRETS_EXIST" = "no" ]; then
  echo "==> Enabling KV v2 and writing secrets..."
  vault secrets enable -path=secret kv-v2

  vault kv put secret/database \
    PROJECT_NAME="${PROJECT_NAME}"


  #vault kv put secret/backend \

  echo "==> Secrets written."
fi

echo "==> Vault is ready."
wait $VAULT_PID