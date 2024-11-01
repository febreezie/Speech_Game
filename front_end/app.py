from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Directory to save text files
SAVE_DIR = 'saved_texts'
os.makedirs(SAVE_DIR, exist_ok=True)  # Create directory if it doesn't exist

# Home route to serve the frontend page
@app.route('/')
def home():
    return render_template('index.html')

# API route to save the text as a file
@app.route('/save-text', methods=['POST'])
def save_text():
    data = request.json.get('textData', '')
    
    # Define the filename
    filename = os.path.join(SAVE_DIR, 'user_input.txt')
    
    # Save data to a text file
    with open(filename, 'w') as file:
        file.write(data)
    
    return jsonify({'message': 'Text saved successfully', 'file': filename})

if __name__ == '__main__':
    app.run(debug=True)
