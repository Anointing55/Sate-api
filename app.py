from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Hello, World!"}

@app.route('/reply', methods=['POST'])
def reply():
    message = request.form.get('message')
    # Implement logic to process the message and scrape the URL
    # Example: You can call another function to handle the scraping
    return {"reply": f"Here is the processed message: {message}"}

if __name__ == '__main__':
    app.run(debug=True)
