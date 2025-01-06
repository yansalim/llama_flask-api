from flask import Flask, request, jsonify
import os
import requests
import zipfile
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Configurations
MODEL_DIR = os.getenv("MODEL_DIR", "./Llama-2-7b-hf")
MODEL_URL = "https://1drv.ms/u/s!Aff226440d8599fa/EqW0CSAzPQdAsRgJoksultEB7WU1CKXOQLdv4Wn7EcUyDw?e=84YqB2"

# Function to download and extract the model if not present
def download_and_extract_model():
    if not os.path.exists(MODEL_DIR):
        print(f"Model directory '{MODEL_DIR}' not found. Downloading...")
        zip_path = "llama_model.zip"
        try:
            # Download the model zip file
            response = requests.get(MODEL_URL, stream=True)
            response.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Download complete. Extracting...")

            # Extract the zip file
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(".")
            print("Model extracted successfully.")

            # Remove the zip file
            os.remove(zip_path)
        except Exception as e:
            print(f"Error downloading or extracting model: {e}")
            if os.path.exists(zip_path):
                os.remove(zip_path)
            raise

# Ensure the model is available
download_and_extract_model()

# Setup model and text generation pipeline
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, torch_dtype=torch.float16, device_map="auto")
text_gen = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    device_map="auto",
)

# Create Flask app
app = Flask("Llama Server")

@app.route('/llama', methods=['POST'])
def generate_response():
    try:
        data = request.get_json()

        # Data Validation
        if not isinstance(data, dict) or 'prompt' not in data or 'max_length' not in data:
            return jsonify({"error": "Missing or invalid required parameters"}), 400

        prompt = data['prompt']
        max_length = int(data['max_length'])
        top_k = data.get('top_k', 10)
        num_return_sequences = data.get('num_return_sequences', 1)

        # Generate text
        sequences = text_gen(
            prompt,
            do_sample=True,
            top_k=top_k,
            num_return_sequences=num_return_sequences,
            eos_token_id=tokenizer.eos_token_id,
            max_length=max_length,
        )

        return jsonify([seq['generated_text'] for seq in sequences])

    except ValueError as ve:
        return jsonify({"error": f"Value error: {str(ve)}"}), 400
    except RuntimeError as re:
        return jsonify({"error": f"Runtime error: {str(re)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"sucess": f"Unexpected error: {str(e)}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)