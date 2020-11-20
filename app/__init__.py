from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

from app import routes, models

admin = Admin(app, name='gifting', template_mode='bootstrap3')
admin.add_view(ModelView(models.Gifter, db.session))
admin.add_view(ModelView(models.Giftee, db.session))
admin.add_view(ModelView(models.StripeCheckoutSession, db.session))

bootstrap = Bootstrap(app)  