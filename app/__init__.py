# =================================================================================================
# File: __init__.py
# =================================================================================================
# Description:
# 
# This file is used to create the application object as an instance of class Flask imported from 
# the flask package.
#
# =================================================================================================

from flask import Flask

app = Flask(__name__)

from app import routes
