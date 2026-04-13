import os
import subprocess

# Couleurs
GREEN = "\033[0;32m"
RED = "\033[0;31m"
CYAN = "\033[0;36m"
RESET = "\033[0m"


def get_container_count():
	cmd = "docker compose ps | grep -c 'Up'"
	return int(subprocess.check_output(cmd, shell=True))

def verify_services(expected, count):
	return count >= expected

def success_return():
	print("\n")
	print(f"{GREEN}", "".center(50, "="), f"{RESET}")
	print(f"{GREEN}", f" ALL MICROSERVICES LAUNCHED ".center(50, "="), f"{RESET}")
	print(f"{GREEN}", "".center(50, "="), f"{RESET}")

def print_failure_logs(services):
	if not services:
		return
	for service in services:
		print("\n")
		print(f"{RED}", "".center(50, "-"), f"{RESET}")
		print(f"{RED}", f" LOGS FOR: {service}".center(50, "-"), f"{RESET}")
		print(f"{RED}", "".center(50, "-"), f"{RESET}")
		print("\n")
		try:
			cmd = f"docker compose logs {service}"
			logs = subprocess.check_output(cmd, shell=True, text=True)
			print(logs)
		except Exception as e:
			print("-" * 50)
			print(f"ERROR COLLECTING LOGS FOR: {service}: {e}".center(50, "-"))
			print("-" * 50)

def get_unhealthy_services():
	unhealthy_names = []
	try:
		cmd = "docker compose ps -a --format '{{.Service}}:{{.Status}}'"
		output = subprocess.check_output(cmd, shell=True).decode().strip()
		if not output:
			return []
		for line in output.split('\n'):
			name, status = line.split(':')
			if "Up" not in status and "running" not in status.lower():
				unhealthy_names.append(name)
		return unhealthy_names
	except Exception:
		return []

def error_return(expected, count):
	nb_error = expected - count
	print(f"{RED}", "".center(50, "="), f"{RESET}")
	print(f"{RED}", f" ERROR ON {nb_error} MICROSERVICES".center(50, "="), f"{RESET}")
	print(f"{RED}", "".center(50, "="), f"{RESET}")
	services = get_unhealthy_services()
	print_failure_logs(services)


def main():
	expected = int(os.getenv("NB_SERVICES", "4"))
	count = get_container_count()

	if verify_services(expected, count):
		success_return()
	else:
		error_return(expected, count)

if __name__ == "__main__":
	main()