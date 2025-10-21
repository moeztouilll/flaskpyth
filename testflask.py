from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running!"

@app.route("/crowdfunding-chat", methods=["POST"])
def crowdfunding_chat():
    try:
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Tu es un chatbot spécialisé en crowdfunding."},
                {"role": "user", "content": prompt}
            ]
        }

        headers = {
            "Authorization": "Bearer 7a77da213aadde6e8c9294a9045bc92c1c7d769703af7bd3c1e4977c6dc643a3fbb1b2f40269f5c027177b834d4b7ccec91de988919a0fbd586bbfaf608d6346",  # <-- Mets ta clé ici
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.zukijourney.com/v1/chat/completions",
            json=payload,
            headers=headers
        )

        if response.status_code != 200:
            return jsonify({"error": response.text}), response.status_code

        data = response.json()
        reply_text = data['choices'][0]['message']['content']

        return jsonify({"reply": reply_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
