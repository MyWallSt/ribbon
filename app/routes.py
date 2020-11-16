from app import app
from flask import render_template, url_for, redirect, request
from app.forms import DetailsForm
import stripe
from urllib.parse import urljoin
from app.utils import Utils

###
# Landing pages
###

@app.route('/')
@app.route('/index')
def index():
    return mywallst()

@app.route('/mywallst/')
def mywallst():
    return render_template('welcome.html', variant="MyWallSt", details_link=url_for('mywallst_details'))

@app.route('/horizon/')
def horizon():
    return render_template('welcome.html', variant="Horizon")


###
# Detail pages
###
@app.route('/mywallst/details/', methods=['GET', 'POST'])
def mywallst_details():
    form = DetailsForm()
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            print(err)

    if form.validate_on_submit():
        print("validate_on_submit")
        return redirect(url_for('payment_page'))
    else:
        print("else")
    return render_template('details.html', variant="MyWallSt", form=form)


###
# Payment handling pages
###
@app.route('/mywallst/payment', methods=['GET'])
def payment_page():
    session = create_session_for_mywallst_payment()
    return render_template('payment.html', session=session)

@app.route('/mywallst/purchased', methods=['GET'])
def purchased():
    if 'session_id' in request.args:
        process_session_data(request)
    return render_template('purchased.html')


###
# Helper methods
###
def create_session_for_mywallst_payment():
    base_url = request.url_root

    plan_id = app.config['STRIPE_MYWALLST_PLAN_ID']
    success_url =  urljoin(base_url, url_for('purchased') + "?session_id={CHECKOUT_SESSION_ID}")
    cancel_url = urljoin(base_url, url_for('index'))

    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': plan_id,
            'quantity': 1
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url
    )

    return session

###
# For every purchase that is made, an email is sent to notify the right people.
# Furthermore a record is written to the database, so that we can keep track of the amount of sales.
###
def process_session_data(request):
    try:
        stripe.api_key = app.config['STRIPE_SECRET_KEY']
        session_id = request.args.get('session_id')
        checkout_object = stripe.checkout.Session.retrieve(session_id)
        customer_id = checkout_object["customer"]
        customer = stripe.Customer.retrieve(customer_id)
        customer_email = customer["email"]
        Utils.send_purchase_notification()
    except Exception as e:
        print(e)
        pass;