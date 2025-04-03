import requests
from bs4 import BeautifulSoup
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Hello, World!"}

@app.route('/reply', methods=['POST'])
def reply():
    message = request.form.get('message')
    
    # Extract the URL from the message
    url = extract_url_from_message(message)
    
    if url:
        # Scrape the page content
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        
        return {"reply": f"Here is the title of the page: {title}"}
    
    return {"reply": "No URL found in the message."}

def extract_url_from_message(message):
    import re
    match = re.search(r'(https?://\S+)', message)
    if match:
        return match.group(0)
    return None

if __name__ == '__main__':
    app.run(debug=True)
