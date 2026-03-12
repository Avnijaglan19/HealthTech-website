# =================================================================================================
# File: healthtech.py
# =================================================================================================
# Description:
# 
# This file is purposefully placced at the top level of the project directory to make it easier to 
# run the application. It imports the app object from the app package and runs the Flask 
# application.
#
# =================================================================================================


from app import app


if __name__ == "__main__":
    # run on a different port if port 5000 is occupied
    app.run(port=5008)

# from member of the app package, import the app object and run the Flask application
