from flask import Flask, render_template, request, jsonify
from services.Translator import Translator
from config import AVAILABLE_MODELS
from response import TranslationInput

app = Flask(__name__, static_folder="templates/static", template_folder="templates")

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
    try:
        text = inputs.get("text", "")
        source_lang = inputs.get("source_label", "English")
        target_lang = inputs.get("target_label", "Chinese")
        model = inputs.get("model", "translategemma:4b")  
        source_lang_code = inputs.get("source_lang", "en")
        target_lang_code = inputs.get("target_lang", "cn")
        translation_input = TranslationInput(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
        source_lang_code=source_lang_code,
        target_lang_code=target_lang_code,
        model=model
        )

    except Exception as e:
        print(f"Error parsing input: {e}")
        return jsonify({"error": "Invalid input format"}), 400
    
    translator = Translator()
    translated = translator.translate(translation_input)


    return jsonify({"translated_text": translated})

if __name__ == "__main__":
    app.run(debug=True)
