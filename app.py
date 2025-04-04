from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to get instructions based on the query
def get_instructions(url, query):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Default response if no specific instructions are found
        instructions = "Sorry, I could not find specific instructions for your request."

        # Handle common instruction queries
        query_lower = query.lower()

        if 'signup' in query_lower:
            instructions = "To sign up for this website:\n1. Visit the homepage.\n2. Click 'Sign Up' or 'Register'.\n3. Enter your details and submit."

        elif 'login' in query_lower:
            instructions = "To log in:\n1. Go to the login page.\n2. Enter your username and password.\n3. Click 'Login'."

        elif 'terms' in query_lower or 'privacy' in query_lower:
            instructions = "To view terms or privacy policy:\n1. Scroll to the bottom of the website.\n2. Click on 'Terms & Conditions' or 'Privacy Policy'."

        elif 'subscription' in query_lower or 'pricing' in query_lower:
            instructions = "To check subscription plans or pricing:\n1. Look for a 'Pricing' or 'Plans' tab.\n2. Click on it to view available options."

        return instructions

    except requests.exceptions.RequestException:
        return "I couldn't fetch specific instructions from the website. Please check the URL and try again."

# API route for handling the query
@app.route('/api/query', methods=['POST'])
def query_handler():
    try:
        data = request.get_json()

        # Extract the URL and query
        query = data.get("query", "")
        url = data.get("url", "")

        if not url.startswith("http"):
            return jsonify({"error": "Invalid or missing URL"}), 400

        # Get response
        response = get_instructions(url, query)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
