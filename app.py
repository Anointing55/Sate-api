from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Function to extract the title of the page from the URL
def extract_title(url):
    try:
        response = requests.get(url)  # Send a GET request to the URL
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content
            title = soup.title.string if soup.title else 'No title found'  # Extract the title tag content
            return title
        else:
            return "Failed to retrieve the page."
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Main endpoint to handle the incoming request
@app.route('/reply', methods=['POST'])
def reply():
    # Get the message from the form data
    message = request.form.get('message')
    
    # Find all URLs in the message using regex
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    
    # If URLs are found in the message, process the first URL
    if urls:
        # Extract the title of the first URL found
        title = extract_title(urls[0])
        return jsonify({"reply": f"Here is the title of the page: {title}"})
    else:
        # If no URL is found in the message
        return jsonify({"reply": "No URL found in the message."})

if __name__ == '__main__':
    app.run(debug=True)
