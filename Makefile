install:
	docker-compose build --no-cache

run:
	docker-compose up --force-recreate

venv:
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

migrate:
	source venv/bin/activate && \
	flask db migrate -m "add tables"

upgrade:
	source venv/bin/activate && \
	flask db upgrade head
