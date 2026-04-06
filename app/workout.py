# =================================================================================================
# File: workout.py
# =================================================================================================
# Description:
# 
# This file is used to initialize the package and make it easier to import modules from the 
# package. It contains the class definitions and functions that are used in the main.py file to 
# generate responses using the OpenAI API. 
#
# =================================================================================================

class Workout(object):

    def __init__(self, diff, duration, goal, equipment, muscleGroup):
        self.__diff = diff 
        self.__duration = duration
        self.__goal = goal
        self.__equipment = equipment
        self.__mGroup = muscleGroup
        self.__prompt = self.PromptGenerator()

# ================================================================================================
#
# set__diff(self, difficulty)
# Purpose: Allows user to set the difficulty of the workout.
# Input: self, difficulty
# Output: n/a
#
# ================================================================================================ 

    def set__diff(self, difficulty):
        self.__diff = difficulty    



    
# ================================================================================================
#
# get__diff(self)
# Purpose: Returns the value of the private variable, __diff, which is the difficulty of the 
# workout.
# Input: self
# Output: self.__diff
#
# ================================================================================================ 

    def get__diff(self):
            return self.__diff
        



# ================================================================================================
#
# set__duration(self, duration)
# Purpose: Allows user to set the private member __duration = duration. 
# Input: self, duration
# Output: n/a
#
# ================================================================================================ 

    def set__duration(self, duration):
        self.__duration = duration  


    
# ================================================================================================
#
# get__duration(self)
# Purpose: Returns the value of the private variable, __duration, which is the duration of the 
# workout.
# Input: self
# Output: self.__duration
#
# ================================================================================================ 

    def get__duration(self):
        return self.__duration
    


# ================================================================================================
#
# set__exercises(self, exercises):
# Purpose: Allows user to set the private member __exercises = exercises. 
# Input: self, exercises
# Output: n/a
#
# ================================================================================================ 

    def set__goal(self, goal):
        self.__goal = goal


    
# ================================================================================================
#
# get__goal(self):
# Purpose: Returns the value of the private variable, __goal, which is the goal for the workout.
# Input: self
# Output: self.__goal
#
# ================================================================================================ 

    def get__goal(self):
        return self.__goal



# ================================================================================================
#
# set__equipment(self, equipment):
# Purpose: Allows the user to set the private member __equipment = equipment. 
# Input: self, equipment
# Output: n/a
#
# ================================================================================================ 

    def set__equipment(self, equipment):
        self.__equipment = equipment


    
# ================================================================================================
#
# get__equipment(self):
# Purpose: Returns the value of the private variable, __equipment, which is the equipment for the 
# workout.
# Input: self
# Output: self.__equipment
#
# ================================================================================================ 

    def get__equipment(self):
        return self.__equipment
    


# ================================================================================================
#
# set__mGroup(self, muscleGroup):
# Purpose: Allows user to set the private member __mGroup = muscleGroup. 
# Input: self, muscleGroup
# Output: n/a
#
# ================================================================================================ 

    def set__mGroup(self, muscleGroup):
        self.__mGroup = muscleGroup


    
# ================================================================================================
#
# get__mGroup(self):
# Purpose: Returns the value of the private variable, __mGroup, which is the muscle group for the 
# workout.
# Input: self
# Output: self.__mGroup
#
# ================================================================================================ 

    def get__mGroup(self):
        return self.__mGroup
    


# ================================================================================================
#
# PromptGenerator(self):
# Purpose: Allows user to generate a prompt for the OpenAI API to generate a workout based on the 
# difficulty, duration, exercises, equipment, and muscle group variables. 
# Input: self, 
# Output: n/a
#
# ================================================================================================ 

    def PromptGenerator(self):
        self.__prompt = "You are a certified strength and conditioning coach. Create a safe, "\
        f"structured workout plan from the following constraints.\n\n" \
        f"Goal: {self.__goal}\n" \
        f"Difficulty: {self.__diff}\n" \
        f"Duration: {self.__duration}\n" \
        f"Target Muscle Group: {self.__mGroup}\n" \
        f"Available Equipment: {self.__equipment}\n\n" \
        "Output requirements:\n" \
        "1) Warm-up (5-10 minutes).\n" \
        "2) Main workout with sets, reps, rest, and exercise cues.\n" \
        "3) Cool-down (3-5 minutes).\n" \
        "4) Mention substitutions using only listed equipment.\n" \
        "5) Keep total session within the requested duration.\n" \
        "6) Return result in clean markdown with clear headings."
    
# ================================================================================================
#
# get__prompt(self):
# Purpose: Returns the value of the private variable, __prompt, which is the prompt for the OpenAI
#  API to generate a workout.
# Input: self
# Output: self.__prompt
#
# ================================================================================================ 

    def get__prompt(self):
        return self.__prompt 