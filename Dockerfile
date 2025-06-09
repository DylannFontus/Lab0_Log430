# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app/src/pos_django

# Define environment variables
ENV PYTHONPATH=/app/src

# Install bash and other dependencies
RUN apt-get update && apt-get install -y \
    bash \
    default-libmysqlclient-dev \
    mariadb-client \
    gcc \
    build-essential \
    pkg-config \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY src/pos_django/ ./
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh
COPY start.sh start.sh
RUN chmod +x start.sh

# Define the command to run your application
CMD ["bash", "wait-for-it.sh", "db:3306", "--", "bash", "start.sh"]
