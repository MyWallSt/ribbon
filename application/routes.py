from application import application
from flask import render_template, url_for, redirect, request
from application.forms import DetailsForm
from application.models import Giftee, Gifter, StripeCheckoutSession
import stripe
from urllib.parse import urljoin
from application.utils import send_purchase_notification
from application import db

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
    return render_template('welcome.html', variant="Horizon")


###
# Detail pages
###
@application.route('/mywallst/details/', methods=['GET', 'POST'])
def mywallst_details():
    form = DetailsForm()
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            print(err)

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        giftee_email = form.giftee_email.data
        personal_note = form.personal_note.data
        send_gift_date = form.send_gift_date.data
        subscription_options = form.subscription_options.data
        gifter_email = form.gifter_email.data
        
        gifter = Gifter(email=gifter_email)
        giftee = Giftee(first_name=first_name, last_name=last_name, email=giftee_email, personal_note=personal_note, send_gift_date=send_gift_date, gift_owner=gifter, subscription_length=subscription_options)
        
        db.session.add(gifter)
        db.session.add(giftee)
        db.session.commit()
        
        return redirect(url_for('payment_page', gifter_id=gifter.id))
    else:
        return render_template('details.html', variant="MyWallSt", form=form)


###
# Payment handling pages
###
@application.route('/mywallst/<gifter_id>/payment', methods=['GET'])
def payment_page(gifter_id):
    gifter = db.session.query(Gifter).filter_by(id=gifter_id).first()
    giftee = db.session.query(Giftee).filter_by(gifter_id=gifter_id).first()
    is_year_subscription = giftee.subscription_length == 12

    session = create_session_for_mywallst_payment(gifter.email, is_year_subscription)

    stripe_checkout_session = StripeCheckoutSession(session_id=session.id, gifter_id=gifter_id)
    db.session.add(stripe_checkout_session)
    db.session.commit() 

    return render_template('payment.html', session=session)

@application.route('/mywallst/purchased', methods=['GET'])
def purchased():
    if 'session_id' in request.args:
        process_session_data(request)
    return render_template('purchased.html')


###
# Admin views
###
@application.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
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
# Helper methods
###
def create_session_for_mywallst_payment(gifter_email, is_year_subscription):
    base_url = request.url_root

    if is_year_subscription:
        plan_id = application.config['STRIPE_MYWALLST_12M_PLAN_ID']
    else:
        plan_id = application.config['STRIPE_MYWALLST_6M_PLAN_ID']

    success_url =  urljoin(base_url, url_for('purchased') + "?session_id={CHECKOUT_SESSION_ID}")
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
def process_session_data(request):
    try:
        stripe.api_key = application.config['STRIPE_SECRET_KEY']
        session_id = request.args.get('session_id')

        stripeCheckoutSession = db.session.query(StripeCheckoutSession).filter_by(session_id=session_id).first()
        gifter = db.session.query(Gifter).filter_by(id=stripeCheckoutSession.gifter_id).first()
        giftee = db.session.query(Giftee).filter_by(gifter_id=gifter.id).first()

        send_purchase_notification(gifter=gifter, giftee=giftee)
    except Exception as e:
        print(e)
        pass