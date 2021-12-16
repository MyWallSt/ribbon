from application import application
from flask import render_template, url_for, redirect, request
from application.forms import AcademyDetailsForm, MyWallStDetailsForm, HorizonDetailsForm
from application.models import Giftee, Gifter, StripeCheckoutSession
import stripe
from urllib.parse import urljoin
from application.utils import send_purchase_notifications, process_webhook, send_test_email
from application import db
import requests
import json

###
# Landing pages

@application.route('/')
@application.route('/index')
def index():
    return mywallst()

@application.route('/mywallst/')
def mywallst():
    return render_template('welcome.html', variant="MyWallSt", details_link=url_for('mywallst_details'))

@application.route('/horizon/')
def horizon():
    return render_template('welcome.html', variant="Horizon", details_link=url_for('horizon_details'))

@application.route('/academy/')
def academy():
    return render_template('/academy/welcome.html', variant="Academy", details_link=url_for('academy_details'))

###
# Detail pages
###
@application.route('/mywallst/details/', methods=['GET', 'POST'])
def mywallst_details():
    form = MyWallStDetailsForm()
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            print(err)

    if form.validate_on_submit():
        gifter_id = save_form_data(form=form)

        return redirect(url_for('payment_page', gifter_id=gifter_id, variant='mywallst'))
    else:
        return render_template('details.html', variant="MyWallSt", form=form)

@application.route('/horizon/details/', methods=['GET', 'POST'])
def horizon_details():
    form = HorizonDetailsForm()
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            print(err)

    if form.validate_on_submit():
        gifter_id = save_form_data(form=form)

        return redirect(url_for('payment_page', gifter_id=gifter_id, variant='horizon'))
    else:

        return render_template('details.html', variant="Horizon", form=form)

@application.route('/academy/details/', methods=['GET', 'POST'])
def academy_details():
    form = AcademyDetailsForm()
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            print(err)

    if form.validate_on_submit():
        gifter_id = save_form_data(form=form)

        return redirect(url_for('payment_page', gifter_id=gifter_id, variant='academy'))
    else:
        return render_template('details.html', variant="Academy", form=form)

###
# Payment handling pages
###
@application.route('/<variant>/<gifter_id>/payment', methods=['GET'])
def payment_page(gifter_id, variant):
    gifter = db.session.query(Gifter).filter_by(id=gifter_id).first()

    base_url = request.url_root
    if variant == "mywallst":
        plan_id = application.config['STRIPE_MYWALLST_12M_PLAN_ID']
        success_url = urljoin(base_url, url_for('payment_complete', variant='mywallst') + "?session_id={CHECKOUT_SESSION_ID}")
    elif variant == "horizon":
        plan_id = application.config['STRIPE_HORIZON_PLAN_ID']
        success_url = urljoin(base_url, url_for('payment_complete', variant='horizon') + "?session_id={CHECKOUT_SESSION_ID}") 
    else:
        plan_id = application.config['STRIPE_ACADEMY_PLAN_ID']
        success_url = urljoin(base_url, url_for('payment_complete', variant='academy') + "?session_id={CHECKOUT_SESSION_ID}") 

    session = create_session(gifter.email, plan_id=plan_id, success_url=success_url)

    stripe_checkout_session = StripeCheckoutSession(session_id=session.id, gifter_id=gifter_id)
    db.session.add(stripe_checkout_session)
    db.session.commit()

    return render_template('payment.html', session=session)
    
@application.route('/<variant>/purchased', methods=['GET'])
def payment_complete(variant):
    if 'session_id' in request.args:
        process_session_data(request=request, variant=variant)

    if variant == "academy":
        return render_template('/academy/purchased.html')
    else:
        return render_template('purchased.html')

###
# Admin views
###
@application.route('/admin/login', methods=['GET', 'POST'])
def login():
    print("Login")
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('invalid username + password')
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


###
# Stripe webhook
###
@application.route('/stripe/webhook', methods=['GET','POST'])
def webhook():
    # TODO do async
    stripe_signature = request.headers.get("Stripe-Signature")
    body = request.data
    return process_webhook(signature=stripe_signature, body=body)

###
# Helper methods
###
def create_session(gifter_email, plan_id, success_url):
    base_url = request.url_root
    cancel_url = urljoin(base_url, url_for('index'))

    stripe.api_key = application.config['STRIPE_SECRET_KEY']

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': plan_id,
            'quantity': 1
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=gifter_email
    )

    return session


###
# For every purchase that is made, an email is sent to notify the right people.
# Furthermore a record is written to the database, so that we can keep track of the amount of sales.
###
def process_session_data(request, variant):
    try:
        stripe.api_key = application.config['STRIPE_SECRET_KEY']
        session_id = request.args.get('session_id')

        stripeCheckoutSession = db.session.query(StripeCheckoutSession).filter_by(session_id=session_id).first()
        gifter = db.session.query(Gifter).filter_by(id=stripeCheckoutSession.gifter_id).first()
        giftee = db.session.query(Giftee).filter_by(gifter_id=gifter.id).first()

        send_purchase_notifications(gifter=gifter, giftee=giftee, variant=variant)
    except Exception as e:
        print(e)
        pass

###
# We store form details in the database in case something goes wrong with the payment. Accessible through the CMS.
# Returns the Giftee record ID 
### 
def save_form_data(form):
    first_name = form.first_name.data
    last_name = form.last_name.data
    giftee_email = form.giftee_email.data
    personal_note = form.personal_note.data
    send_gift_date = form.send_gift_date.data
    gifter_email = form.gifter_email.data

    gifter = Gifter(email=gifter_email)
    giftee = Giftee(first_name=first_name, last_name=last_name, email=giftee_email, personal_note=personal_note, send_gift_date=send_gift_date, gift_owner=gifter)

    db.session.add(gifter)
    db.session.add(giftee)
    db.session.commit()

    return gifter.id