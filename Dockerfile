# Creating the Fastapi app Image
# Using Python as the runtime Image

FROM python:3.10.16-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

COPY . /app/

# Command to run the application 

COPY ./run.sh /app/run.sh

RUN chmod +x /app/run.sh

