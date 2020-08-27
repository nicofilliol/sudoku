import tensorflow as tf
from tensorflow import keras
import cv2
import numpy as np

class SudokuCNN:
    def __init__(self, path=None):
        if path:
            self.model = tf.keras.models.load_model(path)
            self.path = path
        
        else:
            self.model = None
            self.path = None
    
    def create_model(self, path="CNN/sudoku_cnn"):
        self.path = path

        # Create Sequential model
        self.model = keras.Sequential()
        self.model.add(keras.layers.Input(shape=(28, 28, 1)))
        
        # Add Convolutional and Pooling Layer
        self.model.add(keras.layers.Conv2D(32, (5,5), activation="relu", padding="same"))
        self.model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))

        # Add second Convolutional and Pooling Layer
        self.model.add(keras.layers.Conv2D(32, (3,3), activation="relu", padding="same"))
        self.model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))

        # Flatten image and add Dense layer
        self.model.add(keras.layers.Flatten())
        self.model.add(keras.layers.Dense(64, activation="relu"))
        self.model.add(keras.layers.Dropout(0.5))

        # Add second Dense layer
        self.model.add(keras.layers.Dense(64, activation="relu"))
        self.model.add(keras.layers.Dropout(0.5))

        # Add Output layer
        self.model.add(keras.layers.Dense(10, activation="softmax"))

        # Save model
        self.model.save(self.path) 

    def fit_model(self):
        mnist = keras.datasets.mnist
        (train_X, train_y), (test_X, test_y) = mnist.load_data()

        # Add grayscale channel to digits
        train_X = train_X.reshape((train_X.shape[0], 28, 28, 1))
        test_X = test_X.reshape((test_X.shape[0], 28, 28, 1))

        # Normalize values
        train_X = train_X / 255.0
        test_X = test_X / 255.0

        # Convert labels from integers to vector (one-hot encoding)
        train_y = tf.one_hot(train_y, 10)
        test_y = tf.one_hot(test_y, 10)

        # Compile model and fit
        self.model.compile(loss="categorical_crossentropy", optimizer="Adam", metrics=["accuracy"])
        self.model.fit(train_X, train_y, batch_size=128, epochs=10, validation_data=(test_X, test_y))

        # Save model
        self.model.save(self.path)

    def predict(self, img) -> int:
        img = cv2.resize(img, (28, 28))
        img = img / 255.0

        digit = keras.preprocessing.image.img_to_array(img)
        digit = np.expand_dims(digit, axis=0)

        # Predict and classify digit
        pred_index = self.model.predict(digit).argmax() # index of highest probability

        return pred_index