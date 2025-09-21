FROM python:3.11-slim

WORKDIR /app

# system deps se precisar (build tools etc)
RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "datathon.app:app", "--host", "0.0.0.0", "--port", "8000"]