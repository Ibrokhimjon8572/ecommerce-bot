run:
	make format
	docker-compose up --build -d

show:
	docker-compose ps -a

stop:
	docker-compose down

format:
	autopep8 --in-place ./*/*.py ./*.py ./*/*/*.py
	autoflake --in-place --remove-unused-variables --remove-all-unused-imports ./*/*.py ./*.py ./*/*/*.py

messages-uz:
	django-admin makemessages -l uz --ignore env

messages-ru:
	django-admin makemessages -l ru --ignore env

compile-language:
	django-admin compilemessages --ignore env
