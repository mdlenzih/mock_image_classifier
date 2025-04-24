# Mock Image Classifier

This project is part of the Inholland course curriculum focused on AI model deployment.
https://relic-fir-dd0.notion.site/Model-Deployment-Inholland-1cac9328873280acb48efc3423310cc7

This mock image classifier serves as a practical example demonstrating:
- Flask web service implementation
- Docker containerization
- REST API development
- Basic model deployment patterns

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker Desktop (latest version)
- Python 3.8 or higher within Virtual environment (recommended)

## Setup Instructions

### 1. Setting up Python Environment (Optional but Recommended)

### 2. Building the Docker Image
```powershell
# Build the Docker image
docker build -t mock-classifier .
# Run the application
docker run -p 5000:5000 mock-classifier
```

### 3. Testing the API, e.g. with Postman
Open Postman
Create a new request:
Method: POST
URL: http://localhost:5000/predict
In the request:
Go to the "Body" tab
Select "form-data"
Add a key named "file"
Click on the right side of the value field and select "File"
Choose an image file to upload
Click "Send"

## Project Context
This project is designed as a learning tool for the Inholland course, demonstrating:
- Basic Flask application development
- Docker containerization
- REST API implementation

The application runs on port 5000 by default and provides a simple interface for testing image classification functionality.
