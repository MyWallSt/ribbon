# from application import application, routes

# if __name__ == '__main__':
#     application.run(host='0.0.0.0')


from flask import Flask, render_template, request

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'   

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():       
    
    return render_template('welcome.html')

if __name__ == '__main__':
    application.run(host='0.0.0.0')