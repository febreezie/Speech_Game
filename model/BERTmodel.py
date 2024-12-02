from sentence_transformers import SentenceTransformer, util
import os
from datetime import datetime

# Load the Sentence-BERT model
similarity_model = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')

def check_relevance(sentence, topic_description):
    # Generate embeddings for the input sentence and the topic description
    sentence_embedding = similarity_model.encode(sentence)
    topic_embedding = similarity_model.encode(topic_description)

    # Calculate cosine similarity between the sentence and the topic description
    similarity = util.pytorch_cos_sim(sentence_embedding, topic_embedding)[0][0].item()

    # Define relevance levels based on the similarity score
    if similarity > 0.4:
        relevance_level = "Highly Relevant"
    elif similarity > 0.25:
        relevance_level = "Moderately Relevant"
    else:
        relevance_level = "Not Relevant"

    # Provide feedback on the relevance determination
    feedback = generate_feedback(relevance_level, similarity)
    return relevance_level, feedback

def generate_feedback(relevance_level, similarity):
    # Generating feedback based on the relevance level and similarity score
    if relevance_level == "Highly Relevant":
        return f"The sentence is highly relevant with a similarity score of {similarity:.2f}. It aligns well with the topic."
    elif relevance_level == "Moderately Relevant":
        return f"The sentence is moderately relevant with a similarity score of {similarity:.2f}. Consider incorporating more specific terms related to the topic for higher relevance."
    else:
        return f"The sentence is not relevant with a similarity score of {similarity:.2f}. It lacks specific terms or concepts related to the topic."

def process_text_file(input_file_path, output_file_path, topic_description):
    try:
        with open(input_file_path, 'r') as file:
            sentence = file.read().strip()

        relevance_level, feedback = check_relevance(sentence, topic_description)

        with open(output_file_path, 'w') as file:
            file.write(f"Sentence: {sentence}\n")
            file.write(f"Relevance: {relevance_level}\n")
            file.write(f"Feedback: {feedback}\n")
    except Exception as e:
        print(f"An error occurred: {e}")

def determine_general_accuracy(feedback_and_sentence_list):
    #calculate average of accuracy scores
    sum = 0
    # need all of tuple index 1
    for item in feedback_and_sentence_list:
        sum = sum + item[1]
    return sum / (len(feedback_and_sentence_list))

def save_feedback_to_file(output_file_path, feedback_and_sentence_list, topic_description):
    if not os.path.isfile(output_file_path): # check file existence
        raise FileNotFoundError(f"Expected output file at path {output_file_path}, did not find.")
    #File exists
    try:
        with open(output_file_path, 'w') as file: # "with" automatically closes file
            file.write(f"Your topic: {topic_description}\n\n")
            for item in feedback_and_sentence_list:
                file.write(f"Your sentence: {item[0]}\n")
                file.write(f"Relevance Level: {item[1]}\n")
                file.write(f"Feedback: {item[2]}\n")
                file.write("-" * 20 + "\n")
            average_score = determine_general_accuracy(feedback_and_sentence_list)
            file.write(f"\nOverall Score for Topic Accuracy: {average_score}")
        print(f"Feedback saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error in save_feedback_to_file with file {file_path}:\n\t{e}")
       
def get_grandparent_directory():
    current_dir = os.path.abspath(os.getcwd())
    grand_parent_dir = os.path.dirname(os.path.dirname(current_dir))
    # if not parent_dir.endswith(os.sep):
    #     parent_dir += os.sep
    return grand_parent_dir

def generate_output_file():
    try:
        # storing output files in grandparent directory
        grandparent_dir = get_grandparent_directory()
        os.makedirs(grandparent_dir, exist_ok=True) # check dir exists
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") #generate unique filename
        filename = f"output_text_{timestamp}.txt"
        output_file_path = os.path.join(grandparent_dir, filename) #add txt file to path
        return output_file_path
    except Exception as e:
        print(f"Error in creating output file {filename}: {e}")




# Example usage
if __name__ == '__main__':
    input_file_path = 'input.txt'  # File where the input sentence is stored
    output_file_path = generate_output_file()
    topic_description = "activities and aspects of farming, including cultivation of soil for the growing of crops and the rearing of animals to provide food, wool, and other products."
    # process_text_file(input_file_path, output_file_path, topic_description)
    #Delete comment symbol to test locally!

    feedback_and_sentence_list = []

    #process_text_file(input_file_path, output_file_path, topic_description)

    #Delete comment symbol to test locally (comment out line above too)!
    while True:
        user_input = input("Enter a sentence to evaluate or type 'exit' to quit: ")
        if user_input.lower().strip() == 'exit':
            break
        relevance_level, feedback = check_relevance(user_input, topic_description)
        print(f"The sentence relevance is: {relevance_level}. Feedback: {feedback}")
        feedback_and_sentence_list.append((user_input, relevance_level, feedback))

    #Write list to file
    file_path = save_feedback_to_file(output_file_path, feedback_and_sentence_list, topic_description)

    