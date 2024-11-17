from sentence_transformers import SentenceTransformer, util
import os

# Load the Sentence-BERT model
similarity_model = SentenceTransformer('all-distilroberta-v1')

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
    with open(input_file_path, 'r') as file:
        sentence = file.read().strip()

    relevance_level, feedback = check_relevance(sentence, topic_description)

    with open(output_file_path, 'w') as file:
        file.write(f"Sentence: {sentence}\n")
        file.write(f"Relevance: {relevance_level}\n")
        file.write(f"Feedback: {feedback}\n")

# Example usage
if __name__ == '__main__':
    input_file_path = 'input.txt'  # File where the input sentence is stored
    output_file_path = 'output.txt' # File where the output will be written
    topic_description = "activities and aspects of farming, including cultivation of soil for the growing of crops and the rearing of animals to provide food, wool, and other products."
    process_text_file(input_file_path, output_file_path, topic_description)