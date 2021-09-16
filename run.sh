python3 update_html.py &
uvicorn server:app --host 0.0.0.0 --port 5001 --ssl-certfile fullchain.pem --ssl-keyfile privkey.pem
