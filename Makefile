all : 
	docker compose up -d --build

front:
	docker compose build frontend
	docker compose up -d frontend

fclean:
	docker system prune -a

re: fclean all