from flask import Flask, request, jsonify, render_template
import os, sys
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.BERTmodel import process_text_file

app = Flask(__name__)

# topic
TOPIC_DESCRIPTION = "activities and aspects of farming, including cultivation of soil for the growing of crops and the rearing of animals to provide food, wool, and other products."



# Directory to save text files
# SAVE_DIR = 'saved_texts'
# OUTPUT_DIR = 'output_texts'
# os.makedirs(SAVE_DIR, exist_ok=True)  # Create directory if it doesn't exist
# os.makedirs(OUTPUT_DIR, exist_ok=True)



# Home route to serve the frontend page
@app.route('/')
def home():
    return render_template('index.html')

def get_saved_texts_directory():
    try:
        #navigate to the parent directory
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        save_dir = os.path.join(parent_dir, 'saved_texts')
        os.makedirs(save_dir, exist_ok=True)
        return save_dir
    except Exception as e:
        raise RuntimeError(f"Error while locating or creating the 'saved_texts' directory: {str(e)}")

def generate_output_file_path(output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S") #unique, timestamped filename
        filename = f"{timestamp}_output.txt"
        output_file_path = os.path.join(output_dir, filename)
        return output_file_path
    except Exception as e:
        print(f"Error in creating output file {filename}: {e}")


# API route to save the text as a file
@app.route('/save-text', methods=['POST'])
def save_text():
    try:
        data = request.json.get('textData', '')
        #handle errors
        if not data.strip():
            return jsonify({'message': 'No text provided to app.'}), 400
        
        save_dir = get_saved_texts_directory()
        
        # generate unique filename for the inputs
        timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        input_filename = f"{timestamp}_speechToText.txt"
        input_file_path = os.path.join(save_dir, input_filename)

        #save text from STT to a text file
        with open(input_file_path, 'w') as file:
            file.write(data)


        # create the output file for BERT's response
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output_texts'))
        output_file_path = generate_output_file_path(output_dir)

        try:
            process_text_file(input_file_path, output_file_path, TOPIC_DESCRIPTION)
        except Exception as e:
            return jsonify({'message': f'Error with processing user input: {str(e)}'}), 500
        return jsonify({'message': 'Text saved successfully', 'file': output_file_path})
    except Exception as e:
        return jsonify({'message': f"An error occurred saving the speech-to-text file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
