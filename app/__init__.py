from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

login = LoginManager(app)
login.init_app(app)

from app import models
from app.admin import AdminIndexView, CustomAdminView

admin = Admin(app, name='MyWallSt Gifting', index_view=AdminIndexView(),
              template_mode='bootstrap3', base_template='admin/master.html')
admin.add_view(CustomAdminView(models.Gifter, db.session))
admin.add_view(CustomAdminView(models.Giftee, db.session))
admin.add_view(CustomAdminView(models.StripeCheckoutSession, db.session))

bootstrap = Bootstrap(app)  

@login.user_loader
def load_user(id):
    return db.session.query(models.User).get(id)
