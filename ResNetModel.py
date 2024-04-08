""" FIT3162 - MCS13 Code
This file contains the ResNetModel class.
It acts as the first step of optimisation for our Deep Learning Model. 

Optimisations include: 
- Batch Normalisation 
- Dropout Rate

@author Benjamin Leong Tjen Ho
@version 1.0.0
@since 30/03/2024
"""

# ============================================================================================================= #

# Imports
from __future__ import annotations

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, activations

from BaseModel import BaseModel

# ============================================================================================================= #


# Class
class ResNetModel(BaseModel):
    """A simple CNN Model class

    @since 1.0.0

    Attributes:
        name (str):            The name of the model
        width (int):           The width of the model's input
        height (int):          The height of the model's input
        depth (int):           The depth of the model's input (e.g., 3 for RGB images)
        num_classes (int):     The number of possible (output) classes

        activation_func (str): The name of the activation function to be used in the model (excluding softmax on last layer)
        optimiser (Optimizer): The optimisation algorithm function to be used in the model
        batch_size (int):      The size of batches to be used when training
        num_epochs (int):      The number of epochs to be used when training
        verbose (int | bool):  An integer value determining how to output the training progress

        (New!)
        num_blocks (int):      The number of ResNet blocks to add into the model
        feature_maps (int):    The base features maps value for the ResNet blocks (Conv2D layers)
        batch_norm(bool):      Boolean stating if Batch Normalisation is needed in the ResNet blocks
        drop_rate (float):     The dropout rate to use in the Dropout Layers

    Methods:
        build_cnn
        fit
        compute_accuracy
        summary

    Private Method:
        _add

    Static Method:
        _get_optimiser
    """

    # Methods
    def __init__(
        self,
        name: str = "ResNet Model",
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
        num_blocks: int = 3,
        feature_maps: int = 32,
        batch_norm: bool = True,
        drop_rate: float = 0.2,
    ) -> BaseModel:
        """Constructor for the BaseModel class

        @since 1.0.0

        @see BaseModel.__init__

        @param name(str):         The name of the Model
        @param input_width(int):  The width of the input value
        @param input_height(int): The height of the input value
        @param depth(int):        The depth of the input value (e.g., 3 for RGB)
        @param num_classes(int):  The number of (output) classes

        @param activation_func(str): The name of the activation function to be used in the model
        @param optimiser(str):       The name of the optimiser to be used in the model

        @param batch_size(int):      The size of each batch when training the model
        @param num_epochs(int):      The number of epochs when training the model
        @param learning_rate(float): The learning rate when performing back propagation
        @param verbose(int | bool):  An integer value determining how to display the training progress

        @param num_blocks(int):   The number of ResNet blocks that the model will have
        @param feature_maps(int): The base size of feature maps. Increases exponentially for each block
        @param batch_norm(bool):  Boolean stating if Batch Normalisation is needed in the ResNet blocks
        @param drop_rate(float):  The dropout rate of the model for the Dropout layer

        @rtype: ResNetModel
        @return: The new constructed ResNetModel instance
        """
        # Passing old parameters to parent class constructor
        super().__init__(
            name,
            input_width,
            input_height,
            depth,
            num_classes,
            activation_func,
            optimiser,
            batch_size,
            num_epochs,
            learning_rate,
            verbose,
        )

        # Assigning new attributes

        # ResNet Attributes
        self.num_blocks = num_blocks
        self.feature_maps = [feature_maps * (1 << i) for i in range(num_blocks)]
        
        # Batch Normalisation
        self.batch_norm = batch_norm

        # Dropout Layer
        self.drop_rate = drop_rate

    def build_cnn(self):
        """Builds the CNN with a ResNet architecture
        The ResNet architecture is as follows:
            (for each n-th ResNet block)
                Conv2D (32*2**i filters)
                BatchNormalization (if batch_norm == True)
                Activation

                Conv2D (32*2**i filters)
                BatchNormalization (if batch_norm == True)
                Activation

                AveragePooling2D
                Dropout

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

        for i, feature_map in enumerate(self.feature_maps):
            self._add(
                layers.Conv2D(
                    feature_map, (3, 3), padding="same", input_shape=input_shape
                )
            )

            if self.batch_norm:
                self._add(layers.BatchNormalization())

            self._add(layers.Activation(self.activation_func.lower()))

            self._add(layers.Conv2D(feature_map, (3, 3), padding="same"))

            if self.batch_norm:
                self._add(layers.BatchNormalization())

            self._add(layers.Activation(self.activation_func.lower()))

            self._add(layers.AveragePooling2D(pool_size=(2, 2), padding="same"))

            self._add(layers.Dropout(self.drop_rate))

        # Flatten and Softmax
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(self.num_classes, activation="softmax"))

    

# ============================================================================================================= #

# Main function
if __name__ == "__main__":
    pass
