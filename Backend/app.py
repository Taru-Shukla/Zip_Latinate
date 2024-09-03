import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Get the external hostname from the environment variable
external_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

# CORS setup: Allow requests from the external hostname
CORS(app, resources={r"/api/*": {"origins": f"https://{external_hostname}"}})

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