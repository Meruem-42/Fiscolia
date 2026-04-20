from passlib.context import CryptContext


def get_secret(secret_name):
    try:
        path = f"/run/secrets/{secret_name}"

        with open(path, "r") as secret_file:
            return secret_file.read().strip()

    except FileNotFoundError:
        print(f"Error : {secret_name} file does not exist.")
        return None

# PASSWORD POLICY

def check_password(password):
	if not password or len(password) < 8:
		return "Password must be at least 8 char"
	if not any(char.isupper() for char in password):
		return "Password must contain at least one uppercase character"
	if not any(char.islower() for char in password):
		return "Password must contain at least one lowercase character"
	if not any(char.isdigit() for char in password):
		return "Password must contain at least one digit character"
	if password.isalnum():
		return "Password must contain at least one special character"
	return None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
	return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)
