from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, CheckboxInput


# =================================================================================================
#
# This class derives from the SelectMultipleField class and is imported from wtforms which allows
# the user to use multiple checkboxes in Flask. 
#
# =================================================================================================

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class WorkoutForm(FlaskForm):

    # Choices are a list of (value, label) tuples in string values

    equip = MultiCheckboxField('Equipment', 
                               choices=[('barbell', 'Barbell'), ('bench', 'Bench'), ('bodyweight', 'Bodyweight'), 
                                        ('cable machine', 'Cable Machine'), ('dumbbells', 'Dumbbells'), 
                                        ('kettlebell', 'Kettlebell'), ('resistance band', 'Resistance Band'), 
                                        ('treadmill', 'Treadmill'), ('weight plates', 'Weight Plates')], coerce=str)
    
    goal = SelectField('Goal', choices=[('fat loss', 'Fat Loss'), ('muscle gain', 'Muscle Gain'), ('strength', 'Strength')],
                        validators=[DataRequired()])
    
    difficulty = SelectField('Difficulty', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), 
                                                    ('advanced', 'Advanced')], validators=[DataRequired()])
    
    duration = SelectField('Duration', choices=[('15 mins', '15 mins'), ('30 mins', '30 mins'), ('45 mins', '45 mins'), 
                                                ('60 mins', '60 mins')], validators=[DataRequired()])
    
    muscle_group = SelectField('Muscle Group', choices=[('abs', 'Abs'), ('back', 'Back'), ('biceps', 'Biceps'), 
                                                        ('chest', 'Chest'), ('glutes', 'Glutes'), ('hamstrings', 'Hamstrings'), 
                                                        ('quads', 'Quads'), ('shoulders', 'Shoulders'), ('triceps', 'Triceps')], 
                                                        validators=[DataRequired()])
    
    submit = SubmitField('✅ Generate Workout')