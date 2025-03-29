"""PLACEHOLDER"""
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
with open("data/train-SMILES.txt", "r", encoding="utf-8") as file:
    smiles_strings = file.readlines()
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(smiles_strings)
total_chars = len(tokenizer.word_index) + 1
sequences = []
for smile in smiles_strings:
    encoded = tokenizer.texts_to_sequences([smile])[0]
    for i in range(1, len(encoded)):
        sequence = encoded[:i+1]
        sequences.append(sequence)
max_sequence_len = max(len(seq) for seq in sequences)
print("max_sequence_len", max_sequence_len)
sequences = pad_sequences(sequences, maxlen=max_sequence_len, padding="pre")
X, y = sequences[:, :-1], sequences[:, -1]
y = tf.keras.utils.to_categorical(y, num_classes=total_chars)
model = Sequential([
    Embedding(total_chars, 50, input_length=max_sequence_len-1),
    LSTM(10, return_sequences=True),
    LSTM(10),
    Dense(total_chars, activation="softmax")
])
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(X, y, epochs=1, batch_size=64)
def generate_smiles(initial_text, max_length):
    for _ in range(max_length):
        token_list = tokenizer.texts_to_sequences([initial_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding="pre")
        predicted = np.argmax(model.predict(token_list), axis=-1)
        next_char = tokenizer.index_word[predicted[0]]
        initial_text += next_char
        if next_char == "\n":
            break
    return initial_text
generated_smiles = generate_smiles("C", max_sequence_len)
with open("model/output.txt", 'w', encoding='utf-8') as output_file:
    output_file.write(generated_smiles)
