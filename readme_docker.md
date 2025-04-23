# Mock Image Classifier API
A simple Flask application that serves as a mock image classification API, containerized with Docker.

## Prerequisites

- Docker Desktop installed
  - [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
  - [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- [Postman](https://www.postman.com/downloads/) installed

## Windows Instructions

### 1. Building the Docker Image
Open PowerShell and run:
```powershell
# Navigate to the project directory
cd path\to\mock_image_classifier

# Build the Docker image
docker build -t mock-classifier .
```

### 2. Running the Container
```powershell
# Run the container
docker run -p 5000:5000 mock-classifier
```

### 3. Testing the API with Postman
1. Open Postman
2. Create a new request:
   - Method: POST
   - URL: `http://localhost:5000/predict`
3. In the request:
   - Go to the "Body" tab
   - Select "form-data"
   - Add a key named "file"
   - Click on the right side of the value field and select "File"
   - Choose an image file to upload
4. Click "Send"

### 4. Common Docker Commands (Windows)
```powershell
# List all containers
docker ps -a

# Stop a running container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# List all images
docker images

# Remove an image
docker rmi mock-classifier
```



## Troubleshooting

1. **Port already in use**
   ```powershell
   # Try a different port
   docker run -p 5001:5000 mock-classifier
   ```
   Then access the API at `http://localhost:5001`

2. **Docker not running**
   - Make sure Docker Desktop is running
   - Check if the Docker service is started in Services



