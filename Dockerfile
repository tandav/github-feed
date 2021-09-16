FROM python:3

EXPOSE 5001

COPY *.py /app/
COPY *.pem /app/
WORKDIR /app

RUN pip install fastapi uvicorn requests tqdm pipe21 && python3 sheduler.py &

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5001", "--ssl-certfile", "fullchain.pem", "--ssl-keyfile", "privkey.pem"]