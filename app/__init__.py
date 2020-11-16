from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

from app import routes

bootstrap = Bootstrap(app)  