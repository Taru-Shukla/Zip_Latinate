import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# CORS setup: Allow the frontend domain to make requests to the backend
CORS(app, resources={r"/api/*": {"origins": "https://zip-latinate-frontend.onrender.com"}})

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

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', 'https://zip-latinate-frontend.onrender.com')
    return response

if __name__ == '__main__':
    # Bind to the port specified by the PORT environment variable, or use 5000 as a fallback
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)