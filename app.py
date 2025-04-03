from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to get instructions based on the query
def get_instructions(url, query):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Default response for cases where no specific instructions are found
        instructions = "Sorry, I could not find specific instructions for this query."

        # Handle common instructions queries
        if 'signup' in query.lower():
            instructions = "To sign up for this website:\n1. Visit the 'Sign Up' or 'Register' page (usually found on the homepage or in the top-right corner).\n2. Provide your email address, username, and create a password.\n3. Click 'Register' or 'Sign Up'.\n4. Check your email for a verification message and click the confirmation link.\n5. Once confirmed, you can log in with your credentials."
        
        elif 'login' in query.lower():
            instructions = "To log in to this website:\n1. Go to the login page.\n2. Enter your email/username and password.\n3. Click 'Login' to access your account."
        
        elif 'terms' in query.lower() or 'privacy' in query.lower():
            instructions = "To view the terms and conditions or privacy policy:\n1. Scroll to the bottom of the homepage.\n2. Click on the link titled 'Terms & Conditions' or 'Privacy Policy'.\n3. Read through the provided terms."

        elif 'subscription' in query.lower() or 'pricing' in query.lower():
            instructions = "To check subscription plans or pricing:\n1. Visit the pricing or subscription page (usually found in the top menu or footer).\n2. Review the different plans and pricing options.\n3. Choose a plan and follow the instructions to complete the process."
        
        # If no match for query, we respond with default message
        return instructions
    except requests.exceptions.RequestException:
        # If the website cannot be reached, provide fallback generic instructions
        return "I couldn't fetch specific instructions from the website, but here's how things usually work:\n1. Look for the 'Sign Up' or 'Register' page on the homepage.\n2. Enter your details, such as email and password.\n3. Click 'Sign Up' and check your email for verification instructions.\n4. After verification, you should be able to log in."

# API route for handling the query
@app.route('/api/query', methods=['POST'])
def query_handler():
    try:
        # Get JSON data from the POST request
        data = request.get_json()
        
        # Extract the URL and query from the data
        query = data.get("query", "")
        
        if "https://" in query:
            url = query.split("https://")[1].split(" ")[0]
            response = get_instructions(f"https://{url}", query)
            return jsonify({"response": response}), 200
        else:
            return jsonify({"error": "Please provide a valid URL."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
