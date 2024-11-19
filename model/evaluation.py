from sentence_transformers import SentenceTransformer
from datasets import load_dataset
import torch
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.linear_model import LogisticRegression
import numpy as np

# Load the SentenceTransformer model
model = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')

# Load the SNLI dataset
dataset = load_dataset("snli", split="validation").filter(lambda x: x['label'] != -1)  # Filter out examples without a proper label

# Preprocess the data
dataset = dataset.map(lambda x: {'sentence': x['premise'] + " [SEP] " + x['hypothesis']})

# Encode sentences to get embeddings
embeddings = model.encode(dataset['sentence'], convert_to_tensor=True, show_progress_bar=True)

# Since tensors can't be directly used in scikit-learn, convert them to numpy array
embeddings = embeddings.cpu().numpy()

# We'll use a simple classifier to predict the labels from embeddings
classifier = LogisticRegression(max_iter=1000)
classifier.fit(embeddings, dataset['label'])

# Predicting the labels on the same dataset for demonstration (usually you'd split the data)
predictions = classifier.predict(embeddings)

# Calculate evaluation metrics
accuracy = accuracy_score(dataset['label'], predictions)
precision, recall, f1, _ = precision_recall_fscore_support(dataset['label'], predictions, average='macro')

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")

