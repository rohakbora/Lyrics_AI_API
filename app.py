from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure the API key is loaded correctly
if not API_KEY:
    raise ValueError("API key not found in environment. Make sure to set GOOGLE_API_KEY in your .env file.")

genai.configure(api_key=API_KEY)

# Define the generative model
model = genai.GenerativeModel('models/gemini-1.5-flash')

@app.route('/generate-lyrics', methods=['POST'])
def generate_lyrics():
    data = request.json

    prompt = data.get('prompt', 'Write a song about love')

    try:
        response = model.generate_content(prompt)


        generated_content = response.candidates[0].content.parts[0].text.strip()

        # Return the generated lyrics as JSON
        return jsonify({"lyrics": generated_content})

    except Exception as e:
        # Return error message if the API call fails
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
