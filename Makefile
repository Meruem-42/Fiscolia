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
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml up -d --build
	@sleep 2
	@$(MAKE) container_check -s
	@$(MAKE) ps 
	@echo -e "$(YELLOW) Project available at http://localhost:8083 $(RESET)"
	@echo -e "$(GREEN) Dashboard available at http://localhost:8083/kibana/app/dashboards $(RESET)"

clean:
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml down

fclean:
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml down --rmi all
	docker image prune -a
	docker system prune -f


re: clean all

ps:
	docker ps -a -f "name=$(PROJECT_NAME)"

logs:
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml logs -f

# ADR
stop:
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml stop

start:
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml start

adr:
	docker run -it --rm -v $(PWD):/app:Z -w /app \
		python:3.11-slim \
		sh -c "pip install -q questionary && python scripts/create_adr.py"
# 	@python3 ./scripts/create_adr.py 

# TEST/CHECKER 

env_check:
	@python3 ./scripts/env_checker.py

container_check:
	@PROJECT_NAME=$(PROJECT_NAME) python3 ./scripts/container_checker.py

github-actions:
	@$(MAKE)