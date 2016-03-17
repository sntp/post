from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class MailStatus(object):
    SENT = 'sent'
    DRAFT = 'draft'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(70), nullable=False)
    is_authenticated = True
    is_active = True
    is_anonymous = False

    def __init__(self, username, password):
        self.username = username.lower()
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id


class Mail(db.Model):
    __tablename__ = 'mails'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(1024))
    text = db.Column(db.String())
    timestamp = db.Column(db.DateTime(), server_default=db.func.now())
    status = db.Column(db.Enum(*[getattr(MailStatus, name) for name in dir(MailStatus) if not name.startswith('__')],
                               name='mail_status'),
                       nullable=False)
    viewed = db.Column(db.Boolean, server_default='False')
    sender = db.relationship(User, foreign_keys='Mail.sender_id')
    recipient = db.relationship(User, foreign_keys='Mail.recipient_id')

    def __init__(self, sender_id, recipient_id, title, text, status):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.title = title
        self.text = text
        self.status = status
