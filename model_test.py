import json
import pickle
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import load_model
import random
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Remove this import as it's causing issues - you don't need to import from model_train
# from model_train import padded_sequences


with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")


with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)


while True:
    input_text = input("enter your command: ")
    # Fix: Change text_to_sequences to texts_to_sequences
    padded_sequence = pad_sequences(tokenizer.texts_to_sequences([input_text]), maxlen=20, truncating='post')
    result = model.predict(padded_sequence)
    tag = label_encoder.inverse_transform([np.argmax(result)])

    for i in data['intents']:
        if i['tag'] == tag:
            print(np.random.choice(i['responses']))