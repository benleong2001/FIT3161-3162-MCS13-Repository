""" FIT3162: Whitebox Testing, Test 1 - Data Augmentation
This file contains a tester to test the Data Augmentation code from the main model training file

@author Benjamin Leong Tjen Ho
@version 1.1.0
@since 15/05/2024
"""

# ============================================================================================================= #

# Imports
import unittest
import pytest
import numpy as np
from tester_base import TesterBase
from typing import List, Tuple
from numpy.typing import NDArray

import os, sys  # Importing other files

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import DATASET_NAME_MAIN, NEUTRAL_DIR

# ============================================================================================================= #

# Constants
DIM_COUNT = 3
ROW_COUNT = 5
COL_COUNT = 5

MIN_TRANSLATION = -5
MAX_TRANSLATION = 5
OFFSET = 1

IMAGE_INPUT = np.array(
    [
        np.array(
            [[ROW_COUNT * i + j for _ in range(DIM_COUNT)] for j in range(COL_COUNT)]
        )
        for i in range(ROW_COUNT)
    ]
)

# ============================================================================================================= #


# Function to test
def get_neutral_image_data(
    resized_shape: Tuple[int, int] = (64, 64)
) -> Tuple[NDArray[NDArray[NDArray[NDArray[int]]]], NDArray[NDArray[int]]]:
    """This function is the function used to generate the images as np.arrays in the main code file."""
    resized_path = f"{DATASET_NAME_RESIZED}_{resized_shape[0]}/{NEUTRAL_DIR}"

    # File paths of the neutral images
    paths = [os.path.join(resized_path, f) for f in main_dirs]

    faces = []
    ids = []

    for unique_id, path in enumerate(paths):
        for img in [os.path.join(path, f) for f in os.listdir(path)]:
            image = np.array(Image.open(img), "uint8")

            # Translate the image laterally and vertically by a random amount.
            translated_image_lateral = np.roll(image, np.random.randint(-5, 5), axis=1)
            translated_image_vertical = np.roll(image, np.random.randint(-5, 5), axis=0)

            # Add the original, laterally translated, and vertically translated images to the list.
            faces.append(image)
            faces.append(translated_image_lateral)
            faces.append(translated_image_vertical)

            # Add the corresponding labels to the list.
            id = [int(bit == unique_id) for bit in range(len(os.listdir(main_path)))]
            ids.append(id)
            ids.append(id)
            ids.append(id)

    # Return the dataset values
    return np.array(faces), np.array(ids)


def data_aug(
    image: NDArray[NDArray[NDArray[int]]],
) -> List[NDArray[NDArray[NDArray[int]]]]:
    """The Data Augmentation part of the original function
    @param image (ndarray[ndarray[ndarray[int]]]): The input image to be augmented

    @rtype:  List[ndarray[ndarray[ndarray[int]]]]
    @return: A list of 3 images, the original, the laterally translated, the vertically translated
    """
    # Translate
    translated_image_lateral = np.roll(
        image, np.random.randint(MIN_TRANSLATION, MAX_TRANSLATION), axis=1
    )
    translated_image_vertical = np.roll(
        image, np.random.randint(MIN_TRANSLATION, MAX_TRANSLATION), axis=0
    )

    imgs = [image, translated_image_lateral, translated_image_vertical]

    return imgs


# ============================================================================================================= #


# Helper Function
def nparray_3d_to_list(
    nparr_3d: NDArray[NDArray[NDArray[any]]],
) -> List[List[List[any]]]:
    """Converts a 3-Dimensional np array into a 3-Dimensional Python list

    @param nparr_3d (NDArray[NDArray[NDArray[any]]])

    @rtype:  List[List[List[any]]]
    @return: The input in a Python list form
    """
    return [[val.tolist() for val in row] for row in nparr_3d]


def transpose(mat: List[List[any]]) -> List[List[any]]:
    """Transposes the input matrix

    @param mat (List[List[any]]): Some matrix holding any type of values

    @rtype:  List[List[any]]
    @return: The transposed version of the input matrix
    """
    return [[row[col_i] for row in mat] for col_i in range(len(mat[0]))]


# ============================================================================================================= #


# Tester
class TestDataAug(TesterBase):
    """Class of Data Augmentation Tester
    Test Cases
    - Converting Image object into nparray
    - Lateral Translations
    - Vertical Translations
    """

    def test_lateral_translation(self):
        """Test for lateral translation

        Input, x: The nparray equivalent of some image
        Truth, y: Input x but with rows shifted by some value in the range [-5, 5]
        """
        original_img, lateral_img, _ = data_aug(IMAGE_INPUT)
        original_img_list = nparray_3d_to_list(original_img)
        lateral_img_list = nparray_3d_to_list(lateral_img)

        # Consider all possible expected shifts
        for offset in range(MIN_TRANSLATION, MAX_TRANSLATION + OFFSET):
            reset_img = [[*row[offset:], *row[:offset]] for row in lateral_img_list]
            if original_img_list == reset_img:
                return

        self.verification_errors.append("Lateral Translation failed.")

    def test_vertical_translation(self):
        """Test for vertical translation

        Input, x: The nparray equivalent of some image
        Truth, y: Input x but with columns shifted by some value in the range [-5, 5]
        """
        original_img, _, vertical_img = data_aug(IMAGE_INPUT)
        original_cols = transpose(nparray_3d_to_list(original_img))
        vertical_cols = transpose(nparray_3d_to_list(vertical_img))

        # Consider all possible expected shifts
        for offset in range(MIN_TRANSLATION, MAX_TRANSLATION + OFFSET):
            reset_cols = [[*row[offset:], *row[:offset]] for row in vertical_cols]
            if original_cols == reset_cols:
                return

        self.verification_errors.append("Vertical Translation failed.")


# ============================================================================================================= #

# Main Function
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDataAug)
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
