.PHONY: lint test-local run-local initial_load incremental monitor run-in-docker

lint:
	black --check app tests
	flake8 app tests
	mypy app tests/**/*.py

run_local:
	bash ./start.sh
	$(MAKE) initial_load

test_local:
	pytest tests/ --disable-warnings

run_in_docker:
	docker-compose up --build

initial_load:
	python app/workers/initial_loader.py

incremental:
	python app/workers/incremental_loader.py

monitor:
	python app/monitoring/monitor_mms_gaps.py
