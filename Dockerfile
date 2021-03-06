FROM python:3.10.5-bullseye

WORKDIR app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 10131

CMD ["python3", "main.py"]