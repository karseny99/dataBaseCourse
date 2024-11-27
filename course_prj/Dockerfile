FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y postgresql-client

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
