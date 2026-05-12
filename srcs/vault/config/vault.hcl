ui = true

# Storage backend: file (persists to disk, survives restarts)
#Has encrypted storage by default
storage "file" {
  path = "/vault/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = "true"
}

# How Vault announces itself to other services
api_addr = "http://vault:8200"

# Disable memory lock (required in Docker without special privileges)
disable_mlock = true

# Default token TTL
default_lease_ttl = "168h"
max_lease_ttl     = "720h"