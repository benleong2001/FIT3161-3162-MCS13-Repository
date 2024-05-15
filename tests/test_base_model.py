""" FIT3162: Whitebox Testing, Test 2 - BaseModel
This file contains a tester to test the Data Augmentation code from the main model training file

@author Benjamin Leong Tjen Ho
@version 1.1.0
@since 15/05/2024
"""

# ============================================================================================================= #

# Imports
import unittest
import pytest
from tester_base import TesterBase

from tensorflow.keras import layers

import os, sys  # Importing other files

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BaseModel import BaseModel

# ============================================================================================================= #

# Constants
BASE_MODEL_LAYERS = [
    "Conv2D",
    "Conv2D",
    "AveragePooling2D",
    "Conv2D",
    "Conv2D",
    "AveragePooling2D",
    "Flatten",
    "Dense",
]

BASE_MODEL_OUTPUT_SHAPES = [
    [64, 64, 32],
    [64, 64, 32],
    [32, 32, 32],
    [32, 32, 64],
    [32, 32, 64],
    [16, 16, 64],
    [16 * 16 * 64],
    [4],
]

# ============================================================================================================= #


# Tester
class TestBaseModel(TesterBase):
    """Class of Base Model functions Tester
    Test Cases
    - Testing constructor (__init__())
    - Testing build_cnn()
    - Testing model after invoking build_cnn()
    - Testing _add()
    """

    def test_constructor(self):
        """Tests the BaseModel constructor

        Input, x: None
        Truth, y: A BaseModel instance
        """
        # Invoking constructor
        try:
            dummy_model = BaseModel()
        except Exception as e:
            self.verification_errors.append(
                f"BaseModel could not be instantiated: {str(e)}."
            )
            return

        # Verifying type of instance
        try:
            self.assertTrue(isinstance(dummy_model, BaseModel))
        except Exception as e:
            self.verification_errors.append(
                f"The instance created is not an instance of the BaseModel class: {str(e)}"
            )
            return

    def test_build_cnn(self):
        """ Tests the build_cnn() method invokation
        
        Input, x: None
        Truth, y: Nothing happens (no output and no crashing)
        """
        # Invoking build_cnn() method
        try:
            dummy_model = BaseModel()
            dummy_model.build_cnn()
        except Exception as e:
            self.verification_errors.append(
                f"The build_cnn() method cannot be invoked: {str(e)}"
            )
            return

    def test_model(self):
        """ Tests the outcome of build_cnn() method
        
        Input, x: None
        Truth, y: BaseModel.model has the expected layers, each layer having their respective expected shapes
        """
        # Verifying layers
        try:
            dummy_model = BaseModel()
            dummy_model.build_cnn()
            self.assertEqual(
                [type(layer).__name__ for layer in dummy_model.model.layers],
                BASE_MODEL_LAYERS,
            )
        except Exception as e:
            self.verification_errors.append(
                f"The model does not have the expected layers: {str(e)}"
            )
            return

        # Verifying output shapes
        try:
            self.assertEqual(
                [
                    layer.output.shape.as_list()[1:]
                    for layer in dummy_model.model.layers
                ],
                BASE_MODEL_OUTPUT_SHAPES,
            )
        except Exception as e:
            self.verification_errors.append(
                f"The model does not have the expected output Tensor shapes: {str(e)}"
            )
            return

    def test_add(self):
        """ Tests the _add() method

        Input, x: Some layer (from tensorflow.keras.layers module)
        Truth, y: BaseModel.model has a new layer of the expected type
        """
        # Invoking method
        try:
            dummy_model = BaseModel()
            dummy_model.build_cnn()
            dummy_model._add(layers.Activation("relu"))
        except Exception as e:
            self.verification_errors.append(
                f"The _add() method does not add a new layer to the model: {str(e)}"
            )
            return

        # Verifying layers
        try:
            self.assertEqual(
                [type(layer).__name__ for layer in dummy_model.model.layers],
                [*BASE_MODEL_LAYERS, "Activation"],
            )
        except Exception as e:
            self.verification_errors.append(
                f"_add() executed but layer is not added: {str(e)}"
            )


# ============================================================================================================= #

# Main Function
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBaseModel)
    unittest.TextTestRunner(verbosity=0).run(suite)

# ============================================================================================================= #

# Version Overview
"""
1.0.0
- Created the tester file
- Copy pasted the unit function
- Created a Test class for this function
- Tested lateral and vertical translation
"""
