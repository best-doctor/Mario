check:
	flake8 super_mario
	mypy super_mario
	make test
	mdl README.md
	safety check -r requirements.txt

test:
	python -m pytest --cov=super_mario --cov-report=xml -p no:warnings --disable-socket
