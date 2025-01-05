# Use python as base image
FROM python:3.13-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./model.py /app/model.py
#COPY ./Llama-2-7b-hf /app/Llama-2-7b-hf SUBSTITUIR PELO ARQUIVO DO MODELO
COPY ./Llama-2-7b-hf /app/Llama-2-7b-hf

# Install the needed packages
RUN apt-get update && apt-get install -y gcc g++ procps
RUN pip install transformers Flask llama-cpp-python torch tensorflow flax sentencepiece nvidia-pyindex nvidia-tensorrt huggingface_hub accelerate

# Expose port 5000 outside of the container
EXPOSE 5000

# Run llama_7b_chat.py when the container launches
CMD ["python", "model.py"]