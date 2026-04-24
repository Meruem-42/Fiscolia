import os
import subprocess
import sys
import time

# Couleurs
GREEN = "\033[0;32m"
RED = "\033[0;31m"
CYAN = "\033[0;36m"
YELLOW = "\033[0;33m"
RESET = "\033[0m"

def get_expected_count():
    try:
        with open("docker-compose.yml", "r") as f:
            content = f.read()
            return content.count("container_name:")
    except:
        return 0

def get_container_count():
	project = os.getenv("PROJECT_NAME", "fiscolia")
	cmd = f"docker ps --filter 'status=running' --filter 'name=^{project}-' -q | wc -l"
	return int(subprocess.check_output(cmd, shell=True))

def verify_services(expected, count):
	return count >= expected

def success_return():
	print("\n")
	print(f"{GREEN}", "".center(50, "="), f"{RESET}")
	print(f"{GREEN}", f" ALL MICROSERVICES LAUNCHED ".center(50, "="), f"{RESET}")
	print(f"{GREEN}", "".center(50, "="), f"{RESET}")
	sys.exit(0)

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
			cmd = f"docker logs {service}"
			logs = subprocess.check_output(cmd, shell=True, text=True)
			print(logs)
		except Exception as e:
			print("-" * 50)
			print(f"ERROR COLLECTING LOGS FOR: {service}: {e}".center(50, "-"))
			print("-" * 50)

def get_unhealthy_services():
	unhealthy_names = []
	try:
		cmd = "docker ps -a --format '{{.Names}}:{{.Status}}'"
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
	sys.exit(1)


def main():
	expected = get_expected_count()
	count = get_container_count()
	max_retries = 5 

	for attempt in range(max_retries):
		if verify_services(expected, count):
			success_return()
		print(f"{YELLOW}Attempt {attempt + 1}/{max_retries}: {count}/{expected} services running. Retrying...{RESET}")
		time.sleep(5)
		count = get_container_count()
	count = get_container_count()
	error_return(expected, count)

if __name__ == "__main__":
	main()