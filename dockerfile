# Use the official Python 3.11 image as a base
FROM python:3.11-slim

# Install dependencies for psycopg2-binary (optional for psycopg2-binary)
RUN apt-get update && apt-get install -y libpq-dev

# Set the working directory
WORKDIR /app

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and install dependencies
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile

# Copy the application code to the container
COPY . .

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_DB=tango

# Expose the application port
EXPOSE 8000

# Start the FastAPI application
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
