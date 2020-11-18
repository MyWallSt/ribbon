from app import db

class Gifter(db.Model):
    __tablename__ = 'gifter'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    giftee = db.relationship('Giftee', backref='gifter', lazy='dynamic')

    def __repr__(self):
        return '<Gifter {}>'.format(self.email)
        
class Giftee(db.Model):
    __tablename__ = 'giftee'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    personal_note = db.Column(db.Text())
    send_gift_date = db.Column(db.Date())
    gifter_id = db.Column(db.Integer, db.ForeignKey('gifter.id'))

    def __repr__(self):
        return '<Giftee {}>'.format(self.email)
 

