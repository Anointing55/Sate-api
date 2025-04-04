from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Root endpoint to confirm API is running
@app.route('/')
def home():
    return jsonify({"message": "Sate API is live!"})

# Function to get instructions based on the query
def get_instructions(url, query):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Default response
        instructions = "Sorry, I could not find specific instructions."

        # Handle common queries
        query_lower = query.lower()
        if 'signup' in query_lower:
            instructions = "To sign up:\n1. Visit the website\n2. Click 'Sign Up'\n3. Follow the instructions."
        elif 'login' in query_lower:
            instructions = "To log in:\n1. Go to the login page\n2. Enter your credentials\n3. Click 'Login'."
        elif 'terms' in query_lower or 'privacy' in query_lower:
            instructions = "To view terms and privacy:\n1. Check the footer of the website\n2. Click 'Terms' or 'Privacy Policy'."
        elif 'subscription' in query_lower or 'pricing' in query_lower:
            instructions = "To check subscription plans:\n1. Visit the pricing page\n2. Choose a plan."
        
        return instructions
    except requests.exceptions.RequestException:
        return "I couldn't fetch specific instructions. Please check the website manually."

# API route for handling queries
@app.route('/api/query', methods=['POST'])
def query_handler():
    try:
        data = request.get_json()
        query = data.get("query", "")
        url = data.get("url", "")

        if url and "https://" in url:
            response_text = get_instructions(url, query)
        else:
            response_text = "Invalid URL provided."

        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
