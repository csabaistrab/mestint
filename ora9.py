import numpy as np
from sklearn.datasets import load_iris
import pandas as pd
from sklearn.preprocessing import normalize
import tensorflow as tf


from sklearn.utils import shuffle


def one_hot_encode(x: np.ndarray, num_labels: int) -> np.ndarray:
    return np.eye(num_labels)[x]
def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x))


def main():
    iris = load_iris()
    data = iris.data
    labels = iris.target
    print(iris.keys())
    print(data.shape, labels.shape)

    print(labels)
    n_data = normalize(data)
    print(n_data.shape)
    train_test_split_no = int(n_data.shape[0] * 0.8)
    print(train_test_split_no)
    X_train = n_data[:train_test_split_no]
    y_train = labels[:train_test_split_no].astype(int)
    y_train = one_hot_encode(y_train, 3)

    print(X_train.shape, y_train.shape)
    X_test = n_data[train_test_split_no:]
    y_test = labels[train_test_split_no:].astype(int)
    y_test = one_hot_encode(y_test, 3)

    print(X_test.shape, y_test.shape)
    set(labels)
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(3, activation="softmax")
    ])
    model.summary()
    for layer in model.get_weights():
        print(layer.shape)

if __name__ == '__main__':
    main()