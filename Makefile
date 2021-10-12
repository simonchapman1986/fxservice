.PHONY: build
build:
	docker build . -t fxservice:latest

.PHONY: test
test:
	python3 -m pytest -v
.PHONY: format
format:
	black .

.PHONY: coverage
coverage:
	pytest --cov=app tests/