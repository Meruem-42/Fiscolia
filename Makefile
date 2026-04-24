PROJECT_NAME=fiscolia

# Couleurs
GREEN  = \033[0;32m
RED    = \033[0;31m
YELLOW = \033[0;33m
BLUE   = \033[0;34m
CYAN   = \033[0;36m
PURPLE = \033[0;35m
RESET  = \033[0m

all :
	@$(MAKE) env_check
	docker compose -p $(PROJECT_NAME) up -d --build
	@sleep 2
	@$(MAKE) container_check -s


clean:
	docker compose -p $(PROJECT_NAME) down

fclean:
	docker compose -p $(PROJECT_NAME) down --rmi all
	docker system prune -f


re: clean all


# TEST/CHECKER 

env_check:
	@python3 ./scripts/env_checker.py

container_check:
	@PROJECT_NAME=$(PROJECT_NAME) python3 ./scripts/container_checker.py

github-actions:
	@$(MAKE)