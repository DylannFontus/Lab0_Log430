# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code into the container
COPY . .

# Expose the port your application will run on
EXPOSE 5000

# Define the command to run your application
CMD ["python", "helloworld.py"]