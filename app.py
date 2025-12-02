import os, json
from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Use a much smaller model for CPU
MODEL_NAME = os.getenv("HF_MODEL_NAME", "distilgpt2")
PIPELINE = None

@app.get("/api/health")
def health():
    return jsonify(
        status="ok", 
        model=MODEL_NAME,
        pipeline_loaded=PIPELINE is not None
    ), 200

@app.get("/")
def home():
    return render_template("index.html")

def load_pipeline():
    """Load the text generation pipeline"""
    global PIPELINE
    if PIPELINE is None:
        print(f"Loading {MODEL_NAME}...")
        try:
            PIPELINE = pipeline(
                "text-generation",
                model=MODEL_NAME,
                max_new_tokens=100,
                temperature=0.7,
                do_sample=True,
            )
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    return True

@app.post("/api/echo")
def echo():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    return jsonify({"reply": (text + "?") if text else "?"}), 200

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("text") or "").strip()
    if not prompt:
        return jsonify({"reply": "(empty prompt)"}), 200
    
    # Load model if not loaded
    if not load_pipeline():
        return jsonify({"error": "Model failed to load"}), 500
    
    try:
        # Generate response
        outputs = PIPELINE(
            prompt,
            max_new_tokens=50,
            temperature=0.7,
            do_sample=True,
            pad_token_id=50256  # GPT-2 pad token
        )
        
        response = outputs[0]['generated_text']
        
        # Remove the input prompt from response
        if response.startswith(prompt):
            response = response[len(prompt):].strip()
        
        return jsonify({"reply": response or "(no response)"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    # Optional: preload model on startup
    # load_pipeline()
    app.run(host="0.0.0.0", port=port, debug=False)