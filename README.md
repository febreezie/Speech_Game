# Speech_Game

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


#Model
cd into model file

    pip install transformers
    pip install sentence_transformers

run the BERTmodel.py to install BERT backend


#Model training/evaluation
    pip install datasets
    pip install transformers datasets scikit-learn
    pip install transformers[torch]

