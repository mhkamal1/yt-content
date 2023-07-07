FROM python:3.8

WORKDIR /pydocker

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["python", "./app/main.py"]

