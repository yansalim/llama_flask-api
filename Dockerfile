# Use python as base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y wget gcc g++ procps unzip

# Install general Python dependencies
RUN pip install --no-cache-dir \
    transformers \
    Flask \
    llama-cpp-python \
    torch \
    tensorflow \
    flax \
    sentencepiece \
    huggingface_hub \
    accelerate

# Install NVIDIA-specific dependencies
RUN pip install --no-cache-dir nvidia-pyindex && \
    pip install --no-cache-dir nvidia-tensorrt || echo "NVIDIA TensorRT not available for this architecture, skipping installation."

# Expose the port used by the Flask app
EXPOSE 8080

# Set the default command
CMD ["python", "model.py"]