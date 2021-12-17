from flask_wtf import FlaskForm
from wtforms import form, fields, validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, Optional
from application import db
from application.models import User
from werkzeug.security import check_password_hash

class MyWallStDetailsForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired('This field is required')], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
    giftee_email = EmailField('Email address', validators=[DataRequired(),Email('Invalid email')], render_kw={"placeholder": "john.doe@email.com"})
    personal_note = TextAreaField('Personal note', description="Add a personal touch with a message to the person of your choice.")
    send_gift_date = StringField('Send gift on date', validators=[Optional()], description="You can select your preferred date for the gift to be sent. Gift orders will be processed within 2 business days.", render_kw={"placeholder": "yyyy/mm/dd"})
    subscription_options =  RadioField('Choose gift', validators=[DataRequired()], choices=[('12','12-month access to MyWallSt - $99.99')], description="This is a one-off payment, not an ongoing subscription. Following the gift period, the user will need to subscribe to maintain MyWallSt access.")
    gifter_email = EmailField('Gifter email address', validators=[DataRequired(),Email('Invalid email')], render_kw={"placeholder": "jane.doe@email.com"})
    submit = SubmitField('Continue')

class HorizonDetailsForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired('This field is required')], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
    giftee_email = EmailField('Email address', validators=[DataRequired(),Email('Invalid email')], render_kw={"placeholder": "john.doe@email.com"})
    personal_note = TextAreaField('Personal note', description="Add a personal touch with a message to the person of your choice.")
    send_gift_date = StringField('Send gift on date', validators=[Optional()], description="You can select your preferred date for the gift to be sent. Gift orders will be processed within 2 business days.", render_kw={"placeholder": "yyyy/mm/dd"})
    subscription_options =  RadioField('Choose gift', validators=[DataRequired()], choices=[('12','12-month access to Horizon - $999')], description="This is a one-off payment, not an ongoing subscription. Following the gift period, the user will need to subscribe to maintain Horizon access.")
    gifter_email = EmailField('Gifter email address', validators=[DataRequired(),Email('Invalid email')], render_kw={"placeholder": "jane.doe@email.com"})
    submit = SubmitField('Continue')

class AcademyDetailsForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired('This field is required')], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
    giftee_email = EmailField('Email address', validators=[DataRequired(),Email('Invalid email')], render_kw={"placeholder": "john.doe@email.com"})
    personal_note = TextAreaField('Personal note', description="Add a personal touch with a message to the person of your choice.")
    send_gift_date = StringField('Send gift on date', validators=[Optional()], description="You can select your preferred date for the gift to be sent. Gift orders will be processed within 2 business days.", render_kw={"placeholder": "yyyy/mm/dd"})
    subscription_options =  RadioField('Choose gift', validators=[DataRequired()], choices=[('12','1 place on The Fundamentals of Stock Picking course — $399')], description="This is a one-off payment that grants the student access to the MyWallSt Academy course and one year's subscription to MyWallSt. Following the one-year subscription period, the student will need to resubscribe to retain full access to MyWallSt.")
    gifter_email = EmailField('Gifter email address', validators=[DataRequired(),Email('Invalid email')], render_kw={"placeholder": "jane.doe@email.com"})
    submit = SubmitField('Continue')


class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not check_password_hash(user.password_hash, self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(username=self.login.data).first()
