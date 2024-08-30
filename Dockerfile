FROM python:3.10-slim

WORKDIR /app
COPY . /app/

# Set the PYTHONPATH to include the root of the project
ENV PYTHONPATH="/app"

# Install make
RUN apt update && apt install -y make

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
