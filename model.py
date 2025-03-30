"""This module trains a model with data from the "data" directory"""
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
def readlines(path):
    """Read file from path and return a list of lines"""
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines
def writelist(path, list0):
    """Write file at path, where every line is an element from a list"""
    with open(path, "w", encoding="utf-8") as f:
        for l in list0:
            f.write(str(l) + "\n")
train_SMILES = readlines("data/train-SMILES.txt") # The longest SMILES string has 28 characters
test_SMILES = readlines("data/test-SMILES.txt") # 26 characters
validation_SMILES = readlines("data/validation-SMILES.txt") # 27 characters
train_G_atomization = [float(r) for r in readlines("data/train-G_atomization.txt")]
test_G_atomization = [float(r) for r in readlines("data/test-G_atomization.txt")]
validation_G_atomization = [float(r) for r in readlines("data/validation-G_atomization.txt")]
def model(string_list, float_list):
    """Compile and fit a new Sequential model"""
    string_dataset = tf.data.Dataset.from_tensor_slices(string_list)
    float_dataset = tf.data.Dataset.from_tensor_slices(float_list)
    text_vectorization_layer = tf.keras.layers.TextVectorization()
    text_vectorization_layer.adapt(string_dataset)
    units = len(text_vectorization_layer.get_vocabulary())
    model = tf.keras.models.Sequential([
        text_vectorization_layer,
        tf.keras.layers.Embedding(units, units),
        tf.keras.layers.LSTM(units),
        tf.keras.layers.Dense(units)
    ])
    model.compile()
    return model.fit(tf.data.Dataset.zip(string_dataset, float_dataset)).history["loss"]
plt.rcParams["font.family"] = "serif"
plt.figure()
plt.plot(model(train_SMILES, train_G_atomization), label="Train")
plt.plot(model(test_SMILES, test_G_atomization), label="Test")
plt.plot(model(validation_SMILES, validation_G_atomization), label="Validation")
plt.ylabel("Loss")
plt.xlabel("Epoch")
plt.legend()
plt.savefig("model/loss-epoch.png")
