from flask_script import Manager
from app import app
from app import db
from app.models import User
from werkzeug.security import generate_password_hash

manager = Manager(app)

###
# Usage: python script.py create_admin_user [username] [password]
###
@manager.command
def create_admin_user(username, password):
    test_user = User(username=username, password_hashD=generate_password_hash(password))
    db.session.add(test_user)
    db.session.commit()

if __name__ == "__main__":
    manager.run()