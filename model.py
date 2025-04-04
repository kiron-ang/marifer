"""model.py"""
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
def saveplot(metric, history, feature_name):
    """Plot metrics from stringfloatmodel()"""
    plt.rcParams["font.family"] = "serif"
    plt.figure()
    plt.plot(history.history[metric], label="Training Set")
    plt.plot(history.history["val_" + metric], label="Validation Set")
    if metric == "loss":
        plt.ylabel("Loss")
    else:
        plt.ylabel(metric.upper())
    plt.xlabel("Epoch")
    plt.legend()
    plt.savefig(f"model/{metric}-{feature_name}.png")
    plt.close()
def stringfloatmodel(feature_name):
    """Compiles, fits, and trains a model designed to predict a float target from string input"""
    train_smiles = readlines("data/train-SMILES.txt")
    test_smiles = readlines("data/test-SMILES.txt")
    validation_smiles = readlines("data/validation-SMILES.txt")
    train_feature_name = [float(r) for r in readlines(f"data/train-{feature_name}.txt")]
    validation_feature_name = [float(r) for r in readlines(f"data/validation-{feature_name}.txt")]
    text_vectorization_layer = tf.keras.layers.TextVectorization()
    text_vectorization_layer.adapt(train_smiles)
    units = len(text_vectorization_layer.get_vocabulary())
    model = tf.keras.models.Sequential([
        text_vectorization_layer,
        tf.keras.layers.Embedding(units, units // 10),
        tf.keras.layers.LSTM(units // 100),
        tf.keras.layers.Dropout(0.7),
        tf.keras.layers.Dense(1)
    ])
    model.compile(
        loss="huber",
        metrics=["mae", "mape", "mse", "msle"])
    history = model.fit(
        tf.data.Dataset.from_tensor_slices((
            tf.constant(train_smiles), tf.constant(train_feature_name))).batch(1000),
        epochs=10000,
        validation_data=(tf.constant(validation_smiles), tf.constant(validation_feature_name)),
        callbacks=[tf.keras.callbacks.EarlyStopping()]
    )
    saveplot("loss", history, feature_name)
    saveplot("mae", history, feature_name)
    saveplot("mape", history, feature_name)
    saveplot("mse", history, feature_name)
    saveplot("msle", history, feature_name)
    train_predictions = model.predict(tf.constant(train_smiles))
    test_predictions = model.predict(tf.constant(test_smiles))
    validation_predictions = model.predict(tf.constant(validation_smiles))
    writelist(f"model/train-{feature_name}.txt", [p[0] for p in train_predictions])
    writelist(f"model/test-{feature_name}.txt", [p[0] for p in test_predictions])
    writelist(f"model/validation-{feature_name}.txt", [p[0] for p in validation_predictions])
    with open(f"model/summary-{feature_name}.txt", "w", encoding="utf-8") as summary:
        model.summary(print_fn=lambda x: summary.write(x + "\n"))
        summary.write(f"Number of Epochs: {len(history.history["val_loss"])}")
    model.save(f"model/model-{feature_name}.keras")
qm9_features = {
    "A": "float32",
    "B": "float32",
    "C": "float32",
    "Cv": "float32",
    "G": "float32",
    "G_atomization": "float32",
    "H": "float32",
    "H_atomization": "float32",
    "InChI": "string",
    "InChI_relaxed": "string",
    "Mulliken_charges": "Tensor(shape=(29,), dtype=float32)",
    "SMILES": "string",
    "SMILES_relaxed": "string",
    "U": "float32",
    "U0": "float32",
    "U0_atomization": "float32",
    "U_atomization": "float32",
    "alpha": "float32",
    "charges": "Tensor(shape=(29,), dtype=int64)",
    "frequencies": "Tensor(shape=(None,), dtype=float32)",
    "gap": "float32",
    "homo": "float32",
    "index": "int64",
    "lumo": "float32",
    "mu": "float32",
    "num_atoms": "int64",
    "positions": "Tensor(shape=(29, 3), dtype=float32)",
    "r2": "float32",
    "tag": "string",
    "zpve": "float32",
}
for feature, dtype in qm9_features.items():
    if dtype == "float32":
        print(feature.upper())
        stringfloatmodel(feature)
