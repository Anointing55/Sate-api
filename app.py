from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Sate API!"

@app.route('/some-endpoint', methods=['GET', 'POST'])
def some_endpoint():
    if request.method == 'GET':
        return "This is a GET request"
    elif request.method == 'POST':
        param = request.form.get('param', 'no param')
        return f"Received param: {param}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
