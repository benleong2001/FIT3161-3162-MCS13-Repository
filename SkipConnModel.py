""" FIT3162 - MCS13 Code
This file contains the ResNetModel class.
It acts as the first step of optimisation for our Deep Learning Model. 

Optimisations include: 
- Skip Connection
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

from ResNetModel import ResNetModel
from constants import *

# ============================================================================================================= #


# Class
class Residual(tf.keras.Model):
    """Class representing a single Residual Block
    A single block consists of the following layers:
        Conv2D
        BatchNormalisation
        Activation

        Conv2D
        BatchNormalisation
        SkipConnection (may be with Conv2D layer)
        Activation

        AveragePooling2D
        Dropout

    Note:
        Documentation is using UK english. Normalisation refers to Normalization in TensorFlow

    Attributes:
        conv1 (Conv2D)
        conv2 (Conv2D)

        act1 (Activation)
        act2 (Activation)

        bn1 (BatchNormalisation)
        bn2 (BatchNormalisation)

        pool (AveragePooling2D)
        drop_out (Dropout)
    """

    def __init__(
        self,
        num_channels,
        use_conv=False,
        activation_func=RELU,
        drop_rate=0.2,
        input_shape=None,
    ):
        super().__init__()
        # Conv layers
        self.conv1 = layers.Conv2D(
            filters=num_channels, kernel_size=(3, 3), padding="same"
        )

        self.conv2 = layers.Conv2D(
            filters=num_channels, kernel_size=(3, 3), padding="same"
        )

        # Activation
        self.act1 = layers.Activation(activation_func)
        self.act2 = layers.Activation(activation_func)

        # Skip Connection
        self.skip_conn = None
        if use_conv:
            self.skip_conn = layers.Conv2D(filters=num_channels, kernel_size=1)

        # Batch Normalisation
        self.bn1 = layers.BatchNormalization()
        self.bn2 = layers.BatchNormalization()

        # Ending
        self.pool = layers.AveragePooling2D(pool_size=(2, 2), padding="same")
        self.drop_out = layers.Dropout(drop_rate)

    def call(self, X):
        Y = self.act1(self.bn1(self.conv1(X)))
        Y = self.bn2(self.conv2(Y))
        if self.skip_conn:
            X = self.skip_conn(X)
        Y += X
        Y = self.drop_out(self.pool(self.act2(Y)))
        return Y


class ResNetBlock(tf.keras.layers.Layer):
    def __init__(
        self, num_channels, num_residuals, first_block=False, input_shape=None, **kwargs
    ):
        super(ResNetBlock, self).__init__(**kwargs)
        self.residual_layers = [
            Residual(
                num_channels,
                use_conv=(i == 0 and not first_block),
                input_shape=input_shape,
            )
            for i in range(num_residuals)
        ]

    def call(self, X):
        for layer in self.residual_layers:
            X = layer(X)
        return X


class SkipConnModel(ResNetModel):
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
        batch_size: int = 10,
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
            num_blocks,
            feature_maps,
            batch_norm,
            drop_rate,
        )

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

        self.model = models.Sequential(
            [
                tf.keras.layers.Conv2D(
                    filters=32,
                    kernel_size=(3, 3),
                    padding="same",
                    input_shape=input_shape,
                ),
                tf.keras.layers.BatchNormalization(),
                tf.keras.layers.Activation(self.activation_func),
            ]
        )

        for i, feature_map in enumerate(self.feature_maps):
            self._add(
                ResNetBlock(
                    feature_map,
                    1,
                    first_block=not i,
                    input_shape=input_shape if not i else None,
                )
            )

        # Flatten and Softmax
        self._add(layers.Flatten())
        self._add(layers.Dense(self.num_classes, activation="softmax"))


# ============================================================================================================= #

# Main function
if __name__ == "__main__":
    pass
