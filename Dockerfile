FROM python:3.10.5-alpine3.16
WORKDIR /Ms-Contenido-STD
COPY requirements.txt .
RUN pip install -r requirements.txt
