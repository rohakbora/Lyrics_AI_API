from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os 
# Initialize the Flask application and CORS
load_dotenv()
app = Flask(__name__)
# CORS(app)  # Enable CORS
API_KEY = os.environ.get("GOOGLE_API_KEY")
# Configure your Google Generative AI API key
genai.configure(api_key=API_KEY)  # Replace with your actual API key
model = genai.GenerativeModel('gemini-pro')

@app.route('/generate-lyrics', methods=['POST'])
def generate_lyrics():
    data = request.json
    prompt = data.get('prompt', 'Generate lyrics for a song about love.')  # Default prompt if none is provided

    try:
        # Generate content using the model
        response = model.generate_content(prompt)

        # Extract the generated text from the response
        generated_content = response.candidates[0].content.parts[0].text.strip()

        # Return the generated lyrics as JSON
        return jsonify({"lyrics": generated_content})


    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message if the API call fails

if __name__ == '__main__':
    app.run()
