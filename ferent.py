from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["GET"])
def generate():
    key = Fernet.generate_key().decode()
    return jsonify({"key": key})


@app.route("/encrypt", methods=["POST"])
def encrypt():
    try:
        data = request.json
        key = data["key"].encode()
        message = data["message"].encode()

        f = Fernet(key)
        token = f.encrypt(message)

        return jsonify({"result": token.decode()})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})
    
@app.route("/decrypt", methods=["POST"])
def decrypt():
    try:
        data = request.json
        key = data["key"].encode()
        token = data["message"].encode()

        f = Fernet(key)
        msg = f.decrypt(token)

        return jsonify({"result": msg.decode()})
    except Exception:
        return jsonify({"result": "Decryption failed (check the key or text)"})
    
if __name__ == "__main__":
    app.run(debug=True)
    
               