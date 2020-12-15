from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # if application.config['FLASK_ENV'] == "production":
        environ['wsgi.url_scheme'] = 'https'
            
        return self.app(environ, start_response)

application = Flask(__name__)
application.config.from_object(Config)
application.url_map.strict_slashes = False

application.wsgi_app = ReverseProxied(application.wsgi_app)

db = SQLAlchemy(application)
migrate = Migrate(application, db, render_as_batch=True)

login = LoginManager(application)
login.init_app(application)

from application import models
from application.admin import AdminIndexView, CustomAdminView

admin = Admin(application, name='MyWallSt Gifting', index_view=AdminIndexView(),
              template_mode='bootstrap3', base_template='admin/master.html')
admin.add_view(CustomAdminView(models.Gifter, db.session))
admin.add_view(CustomAdminView(models.Giftee, db.session))
admin.add_view(CustomAdminView(models.StripeCheckoutSession, db.session))

bootstrap = Bootstrap(application)  

@login.user_loader
def load_user(id):
    return db.session.query(models.User).get(id)
