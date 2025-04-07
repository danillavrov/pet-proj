FROM python:3.12
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY schemas.py schemas.py
COPY main.py main.py
COPY models.py models.py
COPY proj_pack proj_pack
EXPOSE 8088
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088", "--lifespan=on"]