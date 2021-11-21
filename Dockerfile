FROM python:3-alpine

RUN apk add --update make
COPY template.html Makefile *.py /app/
WORKDIR /app

EXPOSE 5001

RUN pip install fastapi uvicorn requests tqdm pipe21
CMD ["make", "run_no_ssl"]
