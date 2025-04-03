from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Function to extract detailed website information
def extract_website_info(url):
    try:
        response = requests.get(url)  # Send a GET request to the URL
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content

            title = soup.title.string if soup.title else 'No title found'

            description = ''
            desc_tag = soup.find("meta", attrs={"name": "description"})
            if desc_tag and 'content' in desc_tag.attrs:
                description = desc_tag["content"]
            
            keywords = ''
            keywords_tag = soup.find("meta", attrs={"name": "keywords"})
            if keywords_tag and 'content' in keywords_tag.attrs:
                keywords = keywords_tag["content"]
            
            favicon = ''
            icon_tag = soup.find("link", rel="icon") or soup.find("link", rel="shortcut icon")
            if icon_tag and 'href' in icon_tag.attrs:
                favicon = icon_tag["href"]
                if not favicon.startswith("http"):
                    favicon = url + favicon  # Convert relative URL to absolute
            
            # Extract first 200 characters from the page body (preview content)
            content_preview = " ".join(soup.stripped_strings)[:200]

            return {
                "url": url,
                "title": title,
                "description": description,
                "keywords": keywords,
                "favicon": favicon,
                "status_code": response.status_code,
                "content_preview": content_preview
            }
        else:
            return {"error": f"Failed to retrieve the page. Status Code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Main endpoint to handle the incoming request
@app.route('/reply', methods=['POST'])
def reply():
    message = request.form.get('message')
    
    # Find all URLs in the message using regex
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    
    if urls:
        website_info = extract_website_info(urls[0])
        return jsonify({"reply": website_info})
    else:
        return jsonify({"reply": "No URL found in the message."})

if __name__ == '__main__':
    app.run(debug=True)
