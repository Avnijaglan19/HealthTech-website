# =================================================================================================
# File: __init__.py
# =================================================================================================
# Description:
# 
# This file is used to initialize the package and make it easier to import modules from the 
# package. It contains the class definitions and functions that are used in the main.py file to 
# generate responses using the OpenAI API. 
#
# =================================================================================================

class Workout(object):

    def __init__(self, diff, duration):
        self.diff = diff 
        self.duration = duration
        self.exercises = "null"
        self.equipment = "null"



