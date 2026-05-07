FROM docker.io/hashicorp/vault:1.13.3

ARG VAULT_PORT
EXPOSE $VAULT_PORT

CMD ["vault", "server", "-config=/vault/config/vault.json"]