run:
	docker-compose up --build -d

show:
	docker-compose ps -a

stop:
	docker-compose down