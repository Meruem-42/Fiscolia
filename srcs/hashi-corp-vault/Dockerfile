FROM docker.io/hashicorp/vault:2.0

ARG VAULT_PORT
EXPOSE $VAULT_PORT

CMD ["vault", "server", "-config=/vault/config/vault.json"]