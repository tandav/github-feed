python = python3.10

.PHONY: html
html:
	$(python) make_html.py
	# open index.html

.PHONY: run
run:
	$(python) make_html.py &
	uvicorn server:app --host 0.0.0.0 --port 5001 --ssl-certfile fullchain.pem --ssl-keyfile privkey.pem

.PHONY: lint
lint:
	$(python) -m isort --force-single-line-imports .
	$(python) -m flake8 --ignore E221,E501,W503,E701,E704,E741,I100,I201 .

.PHONY: run_no_ssl
run_no_ssl:
	$(python) make_html.py &
	$(python) -m uvicorn server:app --host 0.0.0.0 --port 5001
