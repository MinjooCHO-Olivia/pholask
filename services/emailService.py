from flask import Flask
from flask_mail import Mail, Message

app =Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mjpholask@gmail.com'
app.config['MAIL_PASSWORD'] = 'mjm9748716! '
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def send_email(email, subject, html):

    msg = Message(subject,
                  sender='mjpholask@gmail.com',
                  recipients=[email])
    msg.html = html
    mail.send(msg)

    return "sent"