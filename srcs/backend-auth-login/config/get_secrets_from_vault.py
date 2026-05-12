import os
import json
import requests


def get_vault_token() -> str:
    
    token_file = os.getenv("VAULT_TOKEN_FILE")#, "/vault/data/init.json")
    
    if not os.path.exists(token_file):
        raise RuntimeError(
            f"Token file {token_file} is not found"
            "Check if Vault is initialized"
        )
    
    try:
        with open(token_file, 'r') as f:
            init_data = json.load(f)
            return init_data["root_token"]
    except (KeyError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to read a token from {token_file}: {e}")


def get_secret(path: str) -> dict:

    vault_addr = os.getenv("VAULT_API_ADDR")#, "http://vault:8200")
    vault_token = get_vault_token()
    
    parts = path.split("/", 1)
    if len(parts) == 2:
        mount, key = parts
        api_path = f"{mount}/data/{key}"
    else:
        api_path = f"secret/data/{path}"
    
    url = f"{vault_addr}/v1/{api_path}"
    headers = {"X-Vault-Token": vault_token}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Failed to read a secret '{path}' from Vault: {e}"
        )
    
    data = response.json()
    
    if "data" not in data or "data" not in data["data"]:
        raise RuntimeError(
            f"Secret '{path}' has unexpected response format"
        )
    
    return data["data"]["data"]