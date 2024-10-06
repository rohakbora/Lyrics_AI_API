import google.generativeai as genai
import os
from flask import jsonify, request

# Configure your Google Generative AI API key
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)  # Replace with your actual API key
model = genai.GenerativeModel('gemini-pro')

def generate_lyrics(request):
    if request.method == 'POST':
        data = request.get_json()
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

    return jsonify({"error": "Invalid request method."}), 405  # Method not allowed
