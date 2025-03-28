"""Build qm9/dimenet and create .txt files from its features!"""
import os
import tensorflow_datasets as tfds
def txt(dataset):
    """Creates .txt files from a Tensorflow Dataset!"""
    os.makedirs("data", exist_ok = True)
    dataset = tfds.load(dataset)
    for split in dataset:
        features = []
        for d in dataset[split]:
            for d_ in d:
                features.append(d_)
            break
        for f in features:
            with open("data/" + split + "-" + f + ".txt", "w", encoding = "utf-8") as txtfile:
                for d in dataset[split]:
                    txtfile.write(d[f].numpy())
txt("qm9/dimenet")
