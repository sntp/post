from flask_wtf import Form
from wtforms import StringField, BooleanField, HiddenField
from wtforms.validators import InputRequired, Regexp
from model import User


class LoginForm(Form):
    username = StringField('username', validators=[InputRequired(), Regexp(r'^\S+$')])
    password = StringField('password', validators=[InputRequired()])
    remember = BooleanField('remember', default=False)

    def validate(self):
        if Form.validate(self):
            user = User.query.filter_by(username=self.username.data.lower()).first()
            if user:
                return user.check_password(self.password.data)
        return False


class SignupForm(Form):
    username = StringField('username', validators=[InputRequired(), Regexp(r'^\S+$')])
    password = StringField('password', validators=[InputRequired()])

    def validate(self):
        if Form.validate(self):
            if not User.query.filter_by(username=self.username.data.lower()).count():
                return True
        return False


class SendMailForm(Form):
    recipient = StringField('recipient', validators=[InputRequired(), Regexp(r'^\S+$')])
    title = StringField('title')
    text = StringField('text')
    draft = BooleanField('draft', default=False)
    draft_id = HiddenField('draft_id', validators=[Regexp('^\d*$')])

    def validate(self):
        if Form.validate(self):
            if User.query.filter_by(username=self.recipient.data.lower()).first():
                return True
        return False
