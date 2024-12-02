# AI Speech Game

## Project Overview

The **AI Speech Game** is an interactive platform designed to help users practice and improve their public speaking skills. Users are given a random topic and deliver an impromptu speech, which is transcribed using speech-to-text functionality. Using Natural Language Processing (NLP), the system evaluates the relevance of the speech to the given topic and provides actionable feedback. The platform includes a user-friendly interface, a robust backend, and a fine-tuned BERT-based NLP model for evaluating speech relevance.

---

## Features

- **Speech-to-Text Integration**: Converts user speech into text for analysis.
- **Randomized Topics**: Ensures diverse practice opportunities.
- **NLP-Based Feedback**: Analyzes speech relevance using pre-trained BERT models.
- **Performance Scoring**: Provides detailed metrics to help users refine their skills.

---

## Installation Instructions

### Prerequisites

- **Operating System**: Tested on:
  - Ubuntu 20.04 LTS
  - Windows 10/11
  - macOS 11 (Big Sur) or newer
- **Python**: Version 3.7 or higher is required.
- **Hardware Recommendations**:
  - GPU: NVIDIA GPU with CUDA support (e.g., GTX 1060 or better) for faster NLP processing.
  - RAM: At least 8GB (16GB recommended).
  - Disk Space: 5GB free for model files and datasets.

### Steps to Install

1. **Clone the Repository**
   ```bash
   git clone https://github.com/febreezie/Speech_Game
   cd Speech_Game

2. **Install Model Libraries**
    cd into model file in the Speech_Game.py
    
    ```bash
    cd model
    pip install transformers
    pip install sentence_transformers

3. **Install Evaluation Dependencies**
    ```bash
    pip install datasets
    pip install transformers datasets scikit-learn
    pip install transformers[torch]

#Front end 
cd front_end file
run app.py
    in terminal click link for http://127.0.0.1:5000
    Testing:
        You can either:
            -type in the text box
            -click "start Speech" button and start speaking and click "Stop Speech" when done
        then hit submit
    The speech will now be saved in a file saved in the saved_text folder named user_input.txt

