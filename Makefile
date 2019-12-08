check:
	flake8 super_mario
	mypy super_mario
	make test

test:
	python -m pytest --cov=super_mario --cov-report=xml -p no:warnings --disable-socket
