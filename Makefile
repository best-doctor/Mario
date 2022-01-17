check:
	flake8 super_mario
	mypy super_mario
	safety check -r requirements.txt

test:
	python -m pytest -p no:warnings --disable-socket

coverage:
	python -m pytest --cov=super_mario --cov-report=xml -p no:warnings --disable-socket

lock:
	pip-compile --generate-hashes --no-emit-index-url

install-dev:
	pip-sync requirements.txt
