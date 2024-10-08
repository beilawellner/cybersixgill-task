FROM python:3.12

RUN apt-get update -y 
RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
