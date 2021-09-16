FROM python:3

RUN pip install fastapi uvicorn requests tqdm pipe21

EXPOSE 5001

COPY *.py /app/
COPY *.pem /app/

WORKDIR /app
RUN python3 sheduler.py &
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5001", "--ssl-certfile", "fullchain.pem", "--ssl-keyfile", "privkey.pem"]
