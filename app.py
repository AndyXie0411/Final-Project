from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

app = Flask(__name__)

MODEL_NAME = os.environ.get("HF_MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=os.environ.get("TRANSFORMERS_CACHE"))
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32, 
    cache_dir=os.environ.get("TRANSFORMERS_CACHE")
)
print("Model loaded.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("text", "")  # matches frontend key "text"

    prompt = f"<|system|>\nYou are a helpful assistant.\n<|user|>\n{user_message}\n<|assistant|>\n"

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    output = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7
    )

    answer = tokenizer.decode(output[0], skip_special_tokens=True)

    if "<|assistant|>" in answer:
        answer = answer.split("<|assistant|>")[-1].strip()

    return jsonify({"reply": answer})  # matches frontend expected key "reply"

@app.route("/api/echo", methods=["POST"])
def echo():
    user_message = request.json.get("text", "")
    return jsonify({"reply": user_message})

@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok", 
        "device": "cpu",
        "model": MODEL_NAME,
        "message": "Running on CPU with float32"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
