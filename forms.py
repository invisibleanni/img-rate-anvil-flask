from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    # name = StringField("Name", validators=[DataRequired()])

    unique_id = StringField("Unique ID",
                            validators=[DataRequired(),
                                        Length(min=4, max=20)]
                            )

    session_id = StringField("Session ID",
                             validators=[DataRequired(),
                                         Length(min=1, max=20)]
                             )

    submit = SubmitField("Start")


class QuestionnaireForm(FlaskForm):

    age = IntegerField("Age",
                       validators=[DataRequired()]
                       )

    gender = RadioField(
        "Gender",
        choices=[
            ("M", "Man"),
            ("F", "Woman"),
            ("O", "Other"),
            ("NA", "Prefer Not to Respond"),
        ],
        validators=[DataRequired()],
    )

    vision = RadioField(
        "Do you have normal or corrected to normal vision",
        choices=[
            ("Yes Normal", "Yes"),
            ("No not Normal", "No"),
        ],
        validators=[DataRequired()],
    )

    colorblind = RadioField(
        "Are you color blind?\nhttps://www.colorlitelens.com/ishihara-test.html",
        choices=[
            ("Yes CB", "Yes"),
            ("No CB", "No"),
        ],
        validators=[DataRequired()],
    )

    aiexposure = RadioField(
        "Do you have significant exposure to or prior experience with AI generated images?",
        choices=[
            ("Yes Exposure", "Yes"),
            ("No Exposure", "No"),
        ],
        validators=[DataRequired()],
    )

    submit = SubmitField("Submit Answers")
