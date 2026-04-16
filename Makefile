PROJECT_NAME=fiscolia
NB_MICROSERVICES=5


# Couleurs
GREEN  = \033[0;32m
RED    = \033[0;31m
YELLOW = \033[0;33m
BLUE   = \033[0;34m
CYAN   = \033[0;36m
PURPLE = \033[0;35m
RESET  = \033[0m



all :
	docker compose -p $(PROJECT_NAME) up -d --build
	@sleep 2
	@$(MAKE) check -s

front:
	docker compose build frontend
	docker compose up -d frontend

server:
	docker compose build nginx
	docker compose up -d nginx

back:
	docker stop
	docker build -t backend ./backend-auth
	docker run backend

check:
	@PROJECT_NAME=$(PROJECT_NAME) NB_MICROSERVICES=$(NB_MICROSERVICES)  python3 checker.py

clean:
	docker compose -p $(PROJECT_NAME) down

fclean:
	docker compose -p $(PROJECT_NAME) down --rmi all
	docker system prune -f


re: clean all