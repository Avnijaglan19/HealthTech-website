# =================================================================================================
# File: healthtech.py
# =================================================================================================
# Description:
# 
# This file is uses a python class to store configuration settings for the Flask application. It 
# defines a Config class that contains a SECRET_KEY attribute, which is used for securely signing 
# the session cookie and other security-related needs in Flask. The SECRET_KEY is either obtained 
# from an environment variable or set to a default value if the environment variable is not defined.    
#
# =================================================================================================


import os

class Config:
    # General Configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
                                

