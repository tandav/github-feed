html:
	python3 make_html.py
	# open index.html

run:
	docker build -t gfeed .
	docker run -d --rm -p 5001:5001 gfeed
