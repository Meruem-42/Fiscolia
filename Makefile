PROJECT_NAME=fiscolia
RAG_DATABASE_PATH=./srcs/backend-chatbot/config/ma_base_chroma

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
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml --profile chatbot down

fclean:
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml --profile chatbot down -v --rmi all

re: clean all

ps:
	docker ps -a -f "name=$(PROJECT_NAME)"

logs:
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml logs -f

training: env_check
	@echo "$(CYAN)── Building training image ──$(RESET)"
	@mkdir -p $(PWD)/models
	@echo "$(CYAN)── Lancement de l'entraînement ──$(RESET)"
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml run --rm training
	@echo "$(CYAN)── Training container started in detached mode ──$(RESET)"
	@echo "$(CYAN)Access with: docker compose -p $(PROJECT_NAME) -f srcs/docker-compose.yml exec training bash$(RESET)"
	@docker image rm -f fiscolia-training || true
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

create_users: env_check
	docker compose --profile profile-create-user -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml build create-user
	docker compose --profile profile-create-user -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml run --rm create-user
	@docker image rm -f create-user-image || true

vector_db: env_check
# 	@mkdir -p $(PWD)/models/ollama
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml up -d --build ollama
	docker build -t vector-db ./scripts/create_vector_db
	docker run --name vector-db-container --network fiscolia-network -v $(RAG_DATABASE_PATH):/app/ma_base_chroma vector-db
	docker stop vector-db-container
	docker rm vector-db-container
	docker compose -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml down ollama

create_profiles: env_check
	docker compose --profile profile-create-profile -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml build create-profile
	docker compose --profile profile-create-profile -p $(PROJECT_NAME) --env-file .env -f srcs/docker-compose.yml run --rm create-profile
	@docker image rm -f create-profile-image || true

container_check:
	@PROJECT_NAME=$(PROJECT_NAME) python3 ./scripts/container_checker.py

github-actions:
	@$(MAKE)