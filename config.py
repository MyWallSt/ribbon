import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    if os.environ.get('FLASK_ENV') is not None:
        FLASK_ENV = os.environ.get('FLASK_ENV') 
    
    if os.environ.get('SECRET_KEY') is None:
        raise EnvironmentError("No secret key defined") 
    SECRET_KEY = os.environ.get('SECRET_KEY') 

    if os.environ.get('STRIPE_SECRET_KEY') is None:
        raise EnvironmentError("No Stripe secret key defined") 
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') 

    if os.environ.get('STRIPE_PUBLIC_KEY') is None:
        raise EnvironmentError("No Stripe public key defined") 
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY') 

    if os.environ.get('STRIPE_MYWALLST_PLAN_ID') is None:
        raise EnvironmentError("No Stripe MyWallSt plan ID defined") 
    STRIPE_MYWALLST_PLAN_ID = os.environ.get('STRIPE_MYWALLST_PLAN_ID') 

    if os.environ.get('SMTP_HOST') is None:
        raise EnvironmentError("SMTP host is not set") 
    MAIL_SERVER = os.environ.get('SMTP_HOST') 

    if os.environ.get('SMTP_PORT') is None:
        raise EnvironmentError("SMTP port is not set") 
    MAIL_PORT = os.environ.get('SMTP_PORT') 

    if os.environ.get('SMTP_AUTH') is None:
        raise EnvironmentError("SMTP auth is not set") 
    MAIL_USE_SSL = os.environ.get('SMTP_AUTH') 

    if os.environ.get('SMTP_USERNAME') is None:
        raise EnvironmentError("SMTP username is not set") 
    MAIL_USERNAME = os.environ.get('SMTP_USERNAME') 

    if os.environ.get('SMTP_PASSWORD') is None:
        raise EnvironmentError("SMTP password is not set") 
    MAIL_PASSWORD = os.environ.get('SMTP_PASSWORD') 

    if os.environ.get('SENDER_EMAIL') is None:
        raise EnvironmentError("SENDER_EMAIL is not set") 
    SECURITY_EMAIL_SENDER = os.environ.get('SENDER_EMAIL') 

    if os.environ.get('DATABASE_URL') is None:
        raise EnvironmentError("DATABASE_URL is not set") 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 

    SQLALCHEMY_TRACK_MODIFICATIONS = False