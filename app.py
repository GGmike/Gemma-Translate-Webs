from flask import Flask, render_template, request, jsonify
from services import Translator
from config import AVAILABLE_MODELS

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/models", methods=["GET"])
def get_models():
    return jsonify({"models": AVAILABLE_MODELS})

@app.route("/translate", methods=["POST"])
def translate():
    inputs = request.get_json()
    print(f"Received translation request: {inputs}")
    
    text = inputs.get("text", "")
    source_lang = inputs.get("source_lang", "en")
    target_lang = inputs.get("target_lang", "cn")
    model = inputs.get("model", "translategemma:4b")  
    
    translator = Translator()
    # TODO: pass model to translator
    # translated = translator.translate(text, source_lang, target_lang, model)

    # Placeholder response
    translated = f"[Translation of '{text}' from {source_lang} to {target_lang} using {model}]"

    return jsonify({"translated_text": translated})

if __name__ == "__main__":
    app.run(debug=True)
