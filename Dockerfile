FROM python:3-alpine

EXPOSE 5001

COPY template.html run.sh *.py *.pem /app/
WORKDIR /app

RUN pip install fastapi uvicorn requests tqdm pipe21
CMD ["bash", "run.sh"]
