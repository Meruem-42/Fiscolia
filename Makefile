PROJECT_NAME=fiscolia

all :
	docker compose -p $(PROJECT_NAME) up -d --build

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

fclean:
	docker compose -p $(PROJECT_NAME) down --rmi all
	docker system prune -f


re: fclean all