FROM docker.io/hashicorp/vault:1.13.3

ARG VAULT_PORT
EXPOSE $VAULT_PORT

COPY ./init.sh /vault/init.sh
RUN chmod +x /vault/init.sh

CMD ["/vault/init.sh"]