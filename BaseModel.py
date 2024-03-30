""" FIT3162 - MCS13 Code
This file contains the BaseModel class.
It acts as a base line for our Image Classification Deep Learning Model.
Since it is just a base line, its architecture is extremely simple and has no optimisation.

@author Benjamin Leong Tjen Ho
@version 1.0.0
@since 29/03/2024
"""

# ============================================================================================================= #

# Imports
from __future__ import annotations

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, activations

# ============================================================================================================= #


# Class
class BaseModel:
    """A simple CNN Model class

    @since 1.0.0

    Attributes:
        name (str):               The name of the model
        width (int):              The width of the model's input
        height (int):             The height of the model's input
        depth (int):              The depth of the model's input (e.g., 3 for RGB images)
        num_classes (int):        The number of possible (output) classes

        activation_func (str):    The name of the activation function to be used in the model (excluding softmax on last layer)
        optimiser (Optimizer):    The optimisation algorithm function to be used in the model
        batch_size (int):         The size of batches to be used when training
        num_epochs (int):         The number of epochs to be used when training
        verbose (int | bool):     An integer value determining how to output the training progress

    Methods:
        build_cnn
        fit
        compute_accuracy
        summary

    Static Method:
        _get_optimiser
    """

    # Methods
    def __init__(
        self,
        name: str = "Base Model",
        input_width: int = 64,
        input_height: int = 64,
        depth: int = 3,
        num_classes: int = 4,
        activation_func: str = "relu",
        optimiser: str = "adam",
        batch_size: int = 32,
        num_epochs: int = 20,
        learning_rate: float = 0.0001,
        verbose: int | bool = True,
    ) -> BaseModel:
        """Constructor for the BaseModel class

        @since 1.0.0

        @param name(str): The name of the Model
        @param input_width(int): The width of the input value
        @param input_height(int): The height of the input value
        @param depth(int): The depth of the input value (e.g., 3 for RGB)
        @param num_classes(int): The number of (output) classes

        @param activation_func(str): The name of the activation function to be used in the model
        @param optimiser(str): The name of the optimiser to be used in the model

        @param batch_size(int): The size of each batch when training the model
        @param num_epochs(int): The number of epochs when training the model
        @param learning_rate(float): The learning rate when performing back propagation
        @param verbose(int | bool): An integer value determining how to display the training progress

        @rtype: BaseModel
        @return: The new constructed BaseModel instance
        """

        # Basic attributes
        self.name: str = name
        self.width: int = input_width
        self.height: int = input_height
        self.depth: int = depth
        self.num_classes: int = num_classes

        # Model structure attributes
        self.activation_func: str = activation_func

        # Optimiser attribute - also used when setting the model's structure
        self.optimiser: Optimizer = BaseModel._get_optimiser(optimiser, learning_rate)

        # Attributes used when executing training
        self.batch_size: int = batch_size
        self.num_epochs: int = num_epochs

        # Used for printing out progress during training
        # @see https://stackoverflow.com/questions/47902295/what-is-the-use-of-verbose-in-keras-while-validating-the-model
        self.verbose: int | bool = verbose

    def build_cnn(self):
        """Builds the CNN with a simple architecture
        The current architecture is as follows:
            Conv2D (32 filters)
            Conv2D (32 filters)
            AveragePooling2D

            Conv2D (64 filters)
            Conv2D (64 filters)
            AveragePooling2D

            Flatten
            Softmax

        The input shape is determined by the object's attributes.
        Since we use one-hot vector for the expected output, we are using the categorical_crossentropy loss function.

        Note:
            If the expected output was a singular value, then we would use the sparse_categorical_crossentropy
        """
        # Determining the input shape
        input_shape = (self.height, self.width, self.depth)

        self.model = models.Sequential()

        # Block - Conv2D, Conv2D, AveragePooling
        self.model.add(
            layers.Conv2D(
                32,
                (3, 3),
                padding="same",
                activation=self.activation_func,
                input_shape=input_shape,
            )
        )
        self.model.add(
            layers.Conv2D(32, (3, 3), padding="same", activation=self.activation_func)
        )
        self.model.add(layers.AveragePooling2D(pool_size=(2, 2), padding="same"))

        # Block - Conv2D, Conv2D, AveragePooling
        self.model.add(
            layers.Conv2D(64, (3, 3), padding="same", activation=self.activation_func)
        )
        self.model.add(
            layers.Conv2D(64, (3, 3), padding="same", activation=self.activation_func)
        )
        self.model.add(layers.AveragePooling2D(pool_size=(2, 2), padding="same"))

        # Flatten and Softmax
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(self.num_classes, activation="softmax"))

    def fit(self, x_train, y_train, x_val=None, y_val=None, num_epochs=None) -> History:
        """Trains the model with the given training and validation dataset inputs
        The model is trained with the number of epochs determined by the input.
        If None, then the num_epochs attributes is used.

        @since 1.0.0

        @param x_train(ndarray[List[List[int]]]): The training input values
        @param y_train(ndarray[List[int]]):       The corresponding classes for every training input value encoded as one-hot vectors

        @param x_val(ndarray[List[List[int]]]): The validation input values
        @param y_val(ndarray[List[int]]):       The corresponding classes for every validation input value encoded as one-hot vectors

        @param num_epochs(int | None): (Optional) The number of epochs to run during the training.

        @rtype: History
        @return: The results from the training.
                 This would include the all training and validation loss and accuracy metric values.
        """
        # Determining which number of epochs to use
        num_epochs = num_epochs or self.num_epochs

        # Compiling and training the model
        self.model.compile(
            optimizer=self.optimiser,
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )

        self.history = self.model.fit(
            x_train, y_train, epochs=num_epochs, verbose=self.verbose
        )

        # Returning the History object computed from the .fit() function
        return self.history

    def compute_accuracy(self, x_test, y_test) -> str:
        """Computes the accuracy of the model using a testing dataset

        @since 1.0.0

        @param x_test(ndarray[List[List[int]]]): The testing input values
        @param y_test(ndarray[List[int]]):       The corresponding classes for every testing input value encoded as one-hot vectors

        @rtype: str
        @return: The testing loss and accuracy metrics
        """
        # Compute the metric values
        evaluation_results = self.model.evaluate(x_test, y_test)
        metrics = ["loss", "accuracy"]

        # Print out and return the metric values in a singular string value
        print(
            res := "\n".join(
                [
                    f"{metric}: {result}"
                    for metric, result in zip(metrics, evaluation_results)
                ]
            )
        )
        return res

    def summary(self):
        """Outputs the summary of the model"""
        print(self.model.summary())

    # Static Method
    @staticmethod
    def _get_optimiser(optimiser_name: str, learning_rate: float) -> Optimizer:
        """Generates a Keras Optimiser based on the input name
        This function is open for extensions

        @since 1.0.0

        @see https://www.tensorflow.org/api_docs/python/tf/keras/optimizers

        @param optimiser_name(str): The name of the optimiser to be generator
        @param learning_rate(float): The learning rate when performing back propagation

        @rtype: Optimizer
        @return: The optimiser generated
        """
        # Adam Optimiser
        if optimiser_name == "adam":
            return keras.optimizers.Adam(learning_rate)

        # Nadam Optimiser
        elif optimiser_name == "nadam":
            return keras.optimizers.Nadam(learning_rate)

        # Adagrad Optimiser
        elif optimiser_name == "adagrad":
            return keras.optimizers.Adagrad(learning_rate)

        # RMSprop Optimiser
        elif optimiser_name == "rmsprop":
            return keras.optimizers.RMSprop(learning_rate)

        # Adadelta Optimiser
        elif optimiser_name == "adadelta":
            return keras.optimizers.Adadelta(learning_rate)

        # SGD Optimiser - Gradient Descent (with momentum)
        else:
            return keras.optimizers.SGD(learning_rate, momentum=0.9)


# ============================================================================================================= #

# Main function
if __name__ == "__main__":
    pass
