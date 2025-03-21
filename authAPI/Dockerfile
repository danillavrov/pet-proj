FROM python:3.12
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY schemas.py schemas.py
COPY main.py main.py
COPY models.py models.py
COPY key.pem key.pem
COPY cert.pem cert.pem
EXPOSE 8008
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008", "--ssl-keyfile=key.pem", "--ssl-certfile=cert.pem"]