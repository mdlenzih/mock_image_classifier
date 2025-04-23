# Use Python 3.9 with a slim base image to keep the container size small
FROM python:3.9-slim

# Set the working directory inside the container to /app
# All subsequent commands will be run from this directory
WORKDIR /app

# Copy the requirements.txt file from your local machine to the container
# This is done before copying the rest of the app for better layer caching
COPY requirements.txt .

# Install Python dependencies from requirements.txt
# --no-cache-dir reduces the image size by not caching pip packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
# The '.' means copy everything from the current directory
COPY . .

# Inform Docker that the container will listen on port 5000
# This is a documentation feature and doesn't actually publish the port
EXPOSE 5000

# Command to run when the container starts
# Using gunicorn with 2 worker processes and a timeout of 120 seconds
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
