from flask import Flask, request, jsonify
from flask_cors import CORS
from Script import YouTubeSummarizer

app = Flask(__name__)
CORS(app)  # This allows all origins by default

summarizer = YouTubeSummarizer()

@app.route("/", methods=["GET"])
def home():
    return "<p>YouTube Summarizer API is running</p>"

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"error": "Missing 'url' in JSON request body"}), 400

        url = data["url"]
        summary = summarizer.summarize_video(url)
        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
