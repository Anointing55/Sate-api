import requests

# URL of your Sate API (assuming the Flask app is running locally on port 5000)
SATE_API_URL = "http://localhost:5000/api/query"

# Function to handle queries
def handle_query(query):
    try:
        # Send POST request to the Sate API with the user's query
        response = requests.post(SATE_API_URL, json={"query": query})
        
        # If the API request was successful
        if response.status_code == 200:
            data = response.json()

            # Check if the response contains instructions
            if "response" in data:
                return data["response"]
            else:
                return "Sorry, I couldn't get a valid response for your query."
        else:
            return "Error: Could not get a response from the Sate API."
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Main chatbot loop
if __name__ == "__main__":
    while True:
        query = input("User: ").strip().lower()

        if query == "exit":
            print("Sate: Goodbye!")
            break

        # Get response from Sate API
        response = handle_query(query)

        # Print the response from Sate API
        print(f"Sate: {response}\n")
