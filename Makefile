run:
	docker-compose up --build -d

show:
	docker-compose ps -a

format:
	autopep8 --in-place ./*.py ./*/*.py
