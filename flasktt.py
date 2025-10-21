from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL publique de ton serveur local via ngrok
LOCAL_FLASK_URL = "https://streamlined-cherri-hysteretically.ngrok-free.dev/process"  # <-- tu remplaceras ici

@app.route("/")
def home():
    return "✅ Flask en ligne fonctionne !"

@app.route("/from-flutterflow", methods=["POST"])
def from_flutterflow():
    try:
        data = request.get_json()
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "Aucun message reçu"}), 400

        # Transfert du message au serveur local
        response = requests.post(LOCAL_FLASK_URL, json={"message": message}, timeout=10)

        # Vérifie la réponse du serveur local
        if response.status_code != 200:
            return jsonify({"error": f"Erreur serveur local: {response.text}"}), 500

        local_reply = response.json().get("reply", "Pas de réponse")
        return jsonify({"reply": local_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
