from application import application
from flask_mail import Mail, Message
from flask import render_template
from smtplib import SMTPException
import stripe
import requests

mail = Mail(application)

def send_purchase_notifications(gifter, giftee):
    send_email(gifter, giftee)
    notify_slack(gifter.email)

def send_email(gifter, giftee):
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


###
# Process webhook function for Stripe. This function will process information sent to it
#    Args:
#        signature (string): header signature
#        body (object): body of the request
###
def process_webhook(signature, body):
    print("signature " + signature)
    webhook_secret = application.config['STRIPE_WEBHOOK_SECRET']
    price_12m = application.config['STRIPE_MYWALLST_12M_PLAN_ID']
    price_6m = application.config['STRIPE_MYWALLST_6M_PLAN_ID']
    event = stripe.Webhook.construct_event(body, signature, webhook_secret)
    print(str(event))
    if event.type in ["invoice.finalized"] and event.data.object.items.data.plan.product in [price_12m, price_6m]:
        # Extract the user's email so that it can be included in the notification
        email = retrieve_customer_email(event)
        notify_slack(email=email) #TODO pass email of user

    return ("", 200, None)

def retrieve_customer_email(event): 
    try:
        customer_id = event.data.object.customer
        stripe.api_key = application.config['STRIPE_SECRET_KEY']
        customer = stripe.Customer.retrieve(customer_id)
        print("Customer: " + customer)
        customer_email = customer["email"]
        return customer_email
    except Exception as e:
        print(e)
        return None

def notify_slack(gifter_email):
    slack_token = application.config['SLACK_APP_TOKEN']
    text = "New gift bought by {}. See email or admin panel for more details.".format(gifter_email)
    
    response = requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': "gifting-referral-notifications",
        'text': text
    }).json()
    print(response)

