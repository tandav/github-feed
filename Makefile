html:
	python3 make_html.py
	# open index.html

run:
	python3 make_html.py &
	uvicorn server:app --host 0.0.0.0 --port 5001 --ssl-certfile fullchain.pem --ssl-keyfile privkey.pem

lint:
	python3 -m isort --force-single-line-imports .
	python3 -m flake8 --ignore E221,E501,W503,E701,E704,E741,I100,I201 .

run_no_ssl:
	python3 make_html.py &
	uvicorn server:app --host 0.0.0.0 --port 5001
