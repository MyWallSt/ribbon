import os

class Config(object):
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
    SMTP_HOST = os.environ.get('SMTP_HOST') 

    if os.environ.get('SMTP_PORT') is None:
        raise EnvironmentError("SMTP port is not set") 
    SMTP_PORT = os.environ.get('SMTP_PORT') 

    if os.environ.get('SMTP_SECURE') is None:
        raise EnvironmentError("SMTP secure is not set") 
    SMTP_SECURE = os.environ.get('SMTP_SECURE') 

    if os.environ.get('SMTP_AUTH') is None:
        raise EnvironmentError("SMTP auth is not set") 
    SMTP_SECURE = os.environ.get('SMTP_AUTH') 

    if os.environ.get('SMTP_USERNAME') is None:
        raise EnvironmentError("SMTP username is not set") 
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME') 

    if os.environ.get('SMTP_PASSWORD') is None:
        raise EnvironmentError("SMTP password is not set") 
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD') 

    if os.environ.get('SENDER_EMAIL') is None:
        raise EnvironmentError("SENDER_EMAIL is not set") 
    SENDER_EMAIL = os.environ.get('SMTP_SENDER_EMAILPASSWORD') 
