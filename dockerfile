FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]

LABEL author='Kamanin Y.N.' version=12 broken_keyboards=0
