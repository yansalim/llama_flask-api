# Use python as base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y wget gcc g++ procps unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install general Python dependencies
RUN pip install --no-cache-dir \
    transformers \
    Flask \
    llama-cpp-python \
    torch \
    tensorflow-macos \
    tensorflow-metal \
    flax \
    sentencepiece \
    huggingface_hub \
    accelerate

# Expose the port used by the Flask app
EXPOSE 8080

# Set the default command
CMD ["python", "model.py"]