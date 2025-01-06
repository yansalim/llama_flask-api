
# Llama Server API

This project provides a Flask API to interact with Meta's Llama language model. The implementation supports different environments, including systems with NVIDIA GPUs, macOS with Metal (M1/M2 chips), and AMD processors. Each environment has a dedicated branch with the appropriate configurations.

## Available Branches

- **main**: Default configuration for systems with NVIDIA GPUs.
- **metal**: Optimized configuration for macOS with Metal (M1/M2 chips).
- **amd**: Configuration for systems with AMD processors.

## Prerequisites

Before starting, ensure you have the following components installed:

- [Docker](https://docs.docker.com/get-docker/): To create and manage containers.
- [Docker Compose](https://docs.docker.com/compose/install/): To orchestrate Docker services.
- [Git](https://git-scm.com/downloads): To clone the repository and manage branches.

## Installation Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/llama-server-api.git
   cd llama-server-api
   ```

2. **Select the Appropriate Branch**:

   - For systems with NVIDIA GPUs:

     ```bash
     git checkout main
     ```

   - For macOS with Metal (M1/M2 chips):

     ```bash
     git checkout metal
     ```

   - For systems with AMD GPUs:

     ```bash
     git checkout amd
     ```

3. **Set Up the Llama Model**:

   - Verify that the model directory is present at the path specified in `model.py`. If not, the script will automatically download the model from the provided link.

4. **Build and Start the Container**:

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker image and start the service.

## Testing the API

After starting the container, the API will be available at `http://localhost:8080/llama`. You can test the connection and routes using tools like `curl` or Postman.

**Example with `curl`**:

```bash
curl -X POST http://localhost:8080/llama      -H "Content-Type: application/json"      -d '{
           "prompt": "Hello, how are you?",
           "max_length": 50
         }'
```

**Example with Postman**:

- **URL**: `http://localhost:8080/llama`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
    "prompt": "Hello, how are you?",
    "max_length": 50
  }
  ```

## Official Llama Documentation

For more information about Meta's Llama model, refer to the [official documentation](https://ai.facebook.com/tools/llama/).

---

Follow the instructions above to set up and run the project in your specific environment. If you encounter issues or have questions, refer to the official documentation.
