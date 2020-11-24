from application import application
from flask_mail import Mail, Message
from flask import render_template
from smtplib import SMTPException

mail = Mail(application)

def send_purchase_notification(gifter, giftee):
    sender = application.config['SECURITY_EMAIL_SENDER']
    if application.config['FLASK_ENV'] == "development":
        recipients = ['sammy@mywallst.com']
    else:
        recipients = ['gifting@mywallst.com']

    title = 'MyWallSt gift purchased'
    template = '/email/purchase_notification_email.html'

    msg = Message(title, sender=sender, recipients=recipients)
    template = render_template(template, 
        gifter_email=gifter.email, 
        giftee_email=giftee.email, 
        giftee_first_name=giftee.first_name,
        giftee_last_name=giftee.last_name,
        subscription_length=giftee.subscription_length,
        personal_note=giftee.personal_note,
        send_gift_date=giftee.send_gift_date
        )
    msg.html = template
    try:
        mail.send(msg)
    except SMTPException as e:
        print(e)
        