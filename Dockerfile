FROM python:3.11-slim

WORKDIR /app


COPY ./app .

RUN pip install --no-cache-dir -r requirements.txt


COPY ./app/server.py .

# Porta que expõe o serviço
EXPOSE 7000

CMD ["python", "server.py"]