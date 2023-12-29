from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize

from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, length, equal_to


class AddProductForm(FlaskForm):
    question = StringField("კითხვა", validators=[DataRequired(), length(min=10, max=150)])
    img = FileField("სურათი",
                    validators=[
                        FileRequired(),
                        FileSize(max_size=1024 * 1024 * 20),
                        FileAllowed(["jpg", "png", "jpeg"], message="დაშვებულია მხოლოდ jpg, png და jpeg ფაილები")
                    ])

    submit = SubmitField("დამატება")


class AddAnswerForm(FlaskForm):
    whoanswer = StringField("რა კითხვას პასუხობ", validators=[DataRequired(), length(min=10, max=150)])
    answer = StringField("პასუხი", validators=[DataRequired(), length(min=10, max=300)])
    submit = (SubmitField("დამატება"))


class RegisterForm(FlaskForm):
    username = StringField("შეიყვანეთ იუზერნეიმი")
    password = PasswordField("შეიყვანეთ პაროლი", validators=[
        length(min=8, max=64)
    ])
    repeat_password = PasswordField("გაიმეორეთ პაროლი", validators=[equal_to("password", message="პაროლები არ ემთხვევა")])

    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField("შეიყვანეთ იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[DataRequired(message="პაროლი არ ემთხვევა"), length(min=8, max=64)])
    submit = SubmitField("ავტორიზაცია")
