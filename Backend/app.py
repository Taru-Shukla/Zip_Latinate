from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# Allow all domains for CORS (adjust accordingly)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/convert_name', methods=['POST', 'OPTIONS'])
@cross_origin()
def convert_name():
    if request.method == "OPTIONS":  # Handling preflight for browsers
        return _build_cors_preflight_response()
    elif request.method == "POST":
        name = request.json.get('name', '')
        pig_latin_name = pig_latin(name)
        return _corsify_actual_response(jsonify({"pig_latin_name": pig_latin_name}))

def _build_cors_preflight_response():
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

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
    app.run(host='0.0.0.0', port=port, debug=True)