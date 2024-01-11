FROM python:3.12

WORKDIR /app

COPY src/* /app/

COPY data/testresume.pdf /app/data/

COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

CMD ["python", "app.py"]