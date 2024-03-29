""" Constants File
This file contains constant values which are helpful throughout this repository

@author Benjamin Leong Tjen Ho
@version 1.0.0
@since 29/03/2024
"""

# ============================================================================================================= #

# File paths
DATASET_NAME_MAIN = "RealWorldOccludedFaces-main"
DATASET_NAME_RESIZED = "RealWorldOccludedFaces-resized"
NEUTRAL_DIR = "images/neutral"

# Image
WIDTH = HEIGHT = 224
WIDTHS = HEIGHTS = [96, 128, 224, 256]
RESIZED_SHAPE = (WIDTH, HEIGHT)
RESIZED_SHAPES = list(zip(WIDTHS, HEIGHTS))
DEPTH = 3

# Model
RELU = "relu"
ADAM_OPT = "adam"

# ============================================================================================================= #

# Main functions
if __name__ == "__main__":
    print(RESIZED_SHAPES)

# ============================================================================================================= #

# Version Overview
""" 
1.0.0
- Created file
"""
