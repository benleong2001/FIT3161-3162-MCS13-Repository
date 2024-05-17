""" FIT3162: Testing - Tester Base Class
This file is obtained from a FIT1008 S1 2022 Assignment 2

@author FIT1008 S1 2022 Teaching Team
@modified Benjamin Leong Tjen Ho
@version 1.0.0
@since 09/04/2024
"""

# ============================================================================================================= #

# Imports 
import unittest

# ============================================================================================================= #

class TesterBase(unittest.TestCase):
    def setUp(self):
        """ The 'setUp' method is a frequently used method in unittest, and is called BEFORE every test case is run.
        This is useful when you want to create certain conditions before running a series of tests, without having to
        repeat code within those tests. Used in conjuction with tearDown to help ensure the test is isolated from
        the performance of other tests.

        Here it's just creating storage for any potential raised errors in the tests."""
        self.documentation_errors = []
        self.verification_errors = []
        self.syntax_errors = []
        print(self.id().split(".")[-1])

    def tearDown(self):
        """ The 'tearDown' is another frequently used method in unittest, and is called AFTER every test case is run.
        This is useful when you want to delete created instances or do other required tasks,
        without having to repeat code within those tests. Used in conjuction with setUp to help
        ensure the test is isolated from the performance of other tests.

        Here it's just printing off the errors that may have been stored in our list of errors, as well as the total number
        of errors.
        """
        print(self.__error_str(self.verification_errors, "Verification"))

    def __error_str(self, error_list, error_type):
        s = ""
        for item in error_list:
            s += str(item) + "\n"
        s += f"Number of {error_type} Errors = "+str(len(error_list))
        return s

# ============================================================================================================= #