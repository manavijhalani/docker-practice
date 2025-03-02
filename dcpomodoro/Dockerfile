FROM python:3-alpine3.15

WORKDIR /app
COPY . /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev postgresql-dev

RUN pip install -r requirements.txt

EXPOSE 3000
CMD ["python", "./index.py"]
