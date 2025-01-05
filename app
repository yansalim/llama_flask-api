from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/resource', methods=['GET'])
def get_resource():
    return jsonify({'mensage': 'Llama PDF Reader its on!'})
if __name__ == '__main__':
    app.run(debug=True)
