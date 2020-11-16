from app import app
from flask_mail import Mail, Message
from flask import render_template

mail = Mail(app)

class Utils():
    def send_purchase_notification():
        sender = app.config['SENDER_EMAIL']
        # if app.config['FLASK_ENV'] == "development":
        #     recipients = ['sammy@mywallst.com']
        # else:
        #     recipients = ['sammy@mywallst.com', "luke@mywallst.com"]
        recipients = ['sammy@mywallst.com']

        title = 'MyWallSt gift purchased'
        template = '/email/purchase_notification_email.html'

        msg = Message(title, sender=sender, recipients=recipients)
        msg.html = render_template(template)
        mail.send(msg)
        print("1") 