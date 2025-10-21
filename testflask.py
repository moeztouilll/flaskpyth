from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Route test simple
@app.route("/")
def home():
    return "Server is running!"

# Route POST pour le chatbot crowdfunding
@app.route("/crowdfunding-chat", methods=["POST"])
def crowdfunding_chat():
    try:
        # Récupérer le message de l'utilisateur
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Préparer la requête vers Zuki API (GPT)
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "tu es un chatbot qui repond seulement aux questions de crowdfunding"},
                {"role": "user", "content": user_message}
            ]
        }

        headers = {
            "Authorization": "7a77da213aadde6e8c9294a9045bc92c1c7d769703af7bd3c1e4977c6dc643a3fbb1b2f40269f5c027177b834d4b7ccec91de988919a0fbd586bbfaf608d6346",  # <-- Remplace par ta clé
            "Content-Type": "application/json"
        }

        # Appel POST à l'API GPT
        response = requests.post(
            "https://api.zukijourney.com/v1/chat/completions",
            json=payload,
            headers=headers
        )

        if response.status_code != 200:
            return jsonify({"error": response.text}), response.status_code

        # Récupérer le texte de réponse
        data = response.json()
        choices = data.get("choices", [])
        message = choices[0].get("message", {})
        content = message.get("content", None)

        # Retourner la réponse au client
        return jsonify({"reply": content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lancer le serveur
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
