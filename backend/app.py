from flask import Flask, request, jsonify
import requests
import psycopg2
import json

app = Flask(__name__)

@app.route("/prompt", methods=["POST"])
def handle_prompt():
    user_prompt = request.json.get("prompt")
    
    # Send to Ollama
    response = requests.post("http://ollama:11434/api/generate", json={
        "model": "llama2",
        "prompt": user_prompt
    })

    result = response.json().get("response", "")

    # Index to Elasticsearch
    requests.post("http://elasticsearch:9200/gameplay/_doc", json={
        "prompt": user_prompt,
        "response": result
    })

    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
