from flask import Flask, request, jsonify, render_template, send_from_directory
import spacy
from pathlib import Path
import os

app = Flask(__name__, template_folder='templates')

# Get absolute path to model
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "best_model"

# Load model
try:
    nlp = spacy.load(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load model: {str(e)}")
    exit(1)

@app.route('/')
def home():
    return render_template('client.html')

@app.route('/', methods=['GET', 'POST'])  # Allow both GET and POST
def predict():
    if request.method == 'GET':
        return jsonify({'error': 'Send a POST request with {"text": "your comment"}'}), 400
    
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text parameter'}), 400
    
    doc = nlp(data['text'])
    
    return jsonify({
        'predictions': doc.cats,
        'text': data['text'],
        'overall_score': max(doc.cats.values())
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)