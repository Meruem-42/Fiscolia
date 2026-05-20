def get_secret(secret_name):
    try:
        path = f"/run/secrets/{secret_name}"

        with open(path, "r") as secret_file:
            return secret_file.read().strip()

    except FileNotFoundError:
        print(f"Error : {secret_name} file does not exist.")
        return None