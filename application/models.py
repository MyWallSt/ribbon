from application import db
from flask_login import UserMixin
from application import login
from werkzeug.security import generate_password_hash, check_password_hash

class Gifter(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(120))
    giftee = db.relationship('Giftee', backref='gift_owner', lazy='dynamic')

    def __repr__(self):
        return '<Gifter {} {}>'.format(self.id, self.email)
        
class Giftee(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    personal_note = db.Column(db.Text())
    send_gift_date = db.Column(db.String(120))
    gifter_id = db.Column(db.Integer, db.ForeignKey('gifter.id'))
    subscription_length = db.Column(db.Integer)

    def __repr__(self):
        return '<Gifter {} {}>'.format(self.id, self.email)
 

class StripeCheckoutSession(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    session_id = db.Column(db.String(120))
    gifter_id = db.Column(db.Integer, db.ForeignKey('gifter.id'))

    def __repr__(self):
        return '<StripeCheckoutSession {} {}>'.format(self.id, self.session_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)  