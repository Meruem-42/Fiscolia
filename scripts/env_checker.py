import os
import sys


# Couleurs
GREEN = "\033[0;32m"
RED = "\033[0;31m"
CYAN = "\033[0;36m"
YELLOW = "\033[0;33m"
ORANGE = "\033[0;33m"
PURPLE = "\033[0;35m"
RESET = "\033[0m"

def check_env_variables():
	example_file = ".env.example"
	if not os.path.exists(example_file):
		print(f"{RED}=" * 100)
		print(f"{RED}ERROR: {example_file} not found.")
		print(f"{RED}=" * 100)
		sys.exit(1)

	with open(example_file, "r") as f:
		expected_keys = set()
		for line in f:
			if '=' in line and not line.strip().startswith('#'):
				key = line.split('=')[0].strip()
				expected_keys.add(key)
			   
	env_file = ".env"
	if not os.path.exists(env_file):
		print(f"{RED}=" * 100)
		print(f"{RED}ERROR: {env_file} not found.")
		print(f"{RED}=" * 100)
		sys.exit(1)
	
	actual_keys = set()
	with open(env_file, "r") as f:
		for line in f:
			if '=' in line and not line.strip().startswith('#'):
				key = line.split('=')[0].strip()
				value = line.split('=')[1].strip().strip('"').strip("'")
				
				if value == "":
					print(f"{YELLOW}=" * 100)
					print(f"{YELLOW}WARNING: The variable {PURPLE}{key}{YELLOW} in {PURPLE}{env_file}{YELLOW} is empty. Please set a value for it.{RESET}")
					print(f"{YELLOW}=" * 100)
				actual_keys.add(key)

	print("\n")
	missing_keys = expected_keys - actual_keys
	if missing_keys:
		print(f"{RED}=" * 100)
		print(f"{RED}ERROR: The following environment variables are missing from {PURPLE}{env_file}: {RESET}")
		for key in missing_keys:
			print(f"{RED}- {PURPLE}{key}{RESET}")
		print(f"{RED}=" * 100)
		print(f"{YELLOW}\nPlease add the missing variables to your {PURPLE}{env_file}{RESET}")
		print(f"{YELLOW}Be careful, also check in your github secrets/variables if you are using github actions{RESET}")
		print(f"{YELLOW}👉 Add the missing variables in Settings > Secrets and variables > Actions{RESET}")
		sys.exit(1)
	
	missing_keys = actual_keys - expected_keys
	if missing_keys:
		print(f"{RED}=" * 100)
		print(f"{RED}ERROR: The following environment variables are missing from {PURPLE}{example_file}: {RESET}")
		for key in missing_keys:
			print(f"{RED}- {PURPLE}{key}{RESET}")
		print(f"{RED}=" * 100)
		print(f"{YELLOW}\nPlease if this variables is necessary add it to the {PURPLE}{example_file}{RESET}")
		print(f"{YELLOW}Be careful, also check in your github secrets/variables if you are using github actions{RESET}")
		print(f"{YELLOW}👉 Add the missing variables in Settings > Secrets and variables > Actions{RESET}")
		sys.exit(1)

check_env_variables()