# AI.py
import tensorflow as tf
import numpy as np
from pygame.math import Vector2

class AI:
    def __init__(self):
        self.model = self.create_model() # Create the neural network model

    # Model of the neural network (sequential model with three densely connected layers (Dense). 
    # The first layer has 24 neurons and the activation function "Relu". The second layer also has 24 neurons and the "Relu" activation function. 
    # The third layer has 4 neurons (one for each possible action) and the activation function "softmax".)
    def create_model(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(24, input_shape=(11,), activation='relu'),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(4, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    # Function that is used to train the model
    def train(self, training_data, epochs=10):
        X_train = np.array([i[0] for i in training_data]).reshape(-1, 11)
        y_train = np.array([i[1] for i in training_data])

        self.model.fit(X_train, y_train, epochs=epochs)

    # Function that chooses the best move by predicting it
    def predict(self, state):
        # If the vector state has less than 11 elements, add zeros to reach the correct size
        if len(state) < 11:
            state.extend([0] * (11 - len(state)))
        prediction = self.model.predict(np.array(state).reshape(-1, 11))
        return np.argmax(prediction[0])

    # Function used to get the move that the AI actually use
    def get_action(self, game_state):
        predicted_action_index = self.predict(game_state) # Get the move predicted by AI
        
        directions = [Vector2(0, -1), Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0)] # Map the index of the predicted move to a direction vector
        return directions[predicted_action_index]
