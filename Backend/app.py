import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# CORS setup: Allow requests from the frontend
CORS(app, resources={r"/api/*": {"origins": "https://zip-latinate-frontend.onrender.com"}})

# Explicitly handle OPTIONS request (preflight)
@app.before_request
def handle_options_request():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = 'https://zip-latinate-frontend.onrender.com'
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        response.headers['Access-Control-Max-Age'] = '3600'  # Cache preflight request for an hour
        return response

@app.route('/api/convert_name', methods=['POST'])
def convert_name():
    name = request.json.get('name', '')
    pig_latin_name = pig_latin(name)
    return jsonify({"pig_latin_name": pig_latin_name})

def pig_latin(name):
    vowels = "aeiou"
    name = name.lower()
    words = name.split()
    pig_latin_words = []

    for word in words:
        if any(char.isdigit() for char in word):
            pig_latin_words.append(word)
        elif word[0] in vowels:
            pig_latin_words.append(word + "yay")
        else:
            pig_latin_words.append(word[1:] + word[0] + "ay")
    return " ".join(pig_latin_words)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)