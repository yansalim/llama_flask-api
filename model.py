from flask import Flask, request, jsonify
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Create a Flask object
app = Flask("Llama Server")


model = None
tokenizer = None

@app.route('/llama', methods=['POST'])
def generate_response():
    global model, tokenizer
    try:
        data = request.get_json()
        
        # Create the model and tokenizer if they were not previously created
        if model is None or tokenizer is None:
            # Put the location of to the LLAMA model directory that you downloaded
            model_dir = "/Path-to-your-model-dir/Llama-2-7b-hf"
            # model_dir = "/Path-to-your-model-dir/Llama-2-7b-hf" SUBSTITUIR PELO CAMINHO DO MODELO
                
            # Create the model and tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_dir)
            model = AutoModelForCausalLM.from_pretrained(model_dir)

             # Check if the required fields are present in the JSON data
        if 'prompt' in data and 'max_length' in data:
            prompt = data['prompt']
            max_length = int(data['max_length'])
            
            # Create the pipeline
            text_gen = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                torch_dtype=torch.float16,
                device_map="auto",)


            sequences = text_gen(
                prompt,
                do_sample=True,
                top_k=10,
                num_return_sequences=1,
                eos_token_id=tokenizer.eos_token_id,
                max_length=max_length,
            )

            return jsonify([seq['generated_text'] for seq in sequences])

        else:
            return jsonify({"error": "Missing required parameters"}), 400

    except Exception as e:
        return jsonify({"Error": str(e)}), 500 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
