FROM python:3.12
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY main.py main.py
COPY /home/reftamid/PycharmProjects/pet-proj/proj_pack proj_pack
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]