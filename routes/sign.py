import base64
from datetime import datetime
import wtforms_json
from flask import Blueprint, session, request, url_for, render_template, abort, Flask, Response
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import check_password_hash
from wtforms import Form, StringField, PasswordField, validators
from models.user import User
from resources.database import db_session
from resources.email_confirmation import send_email

sign_bp = Blueprint('sign', __name__)

app =Flask(__name__)

app.config.update(SECRET_KEY='WFVE#G!voP%m')
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

wtforms_json.init()

class RegistrationForm(Form):
    username = StringField('username', [validators.DataRequired(), validators.Length(min=6, max=25)])
    email = StringField('email', [validators.DataRequired(), validators.Email(), validators.Length(min=6, max=35)])
    salted_password = PasswordField('salted_password', [validators.DataRequired(), validators.Length(min=8, max=15)])

@sign_bp.route("/up", methods=['POST'])
def enroll():
    form = RegistrationForm.from_json(request.json)
    if form.validate():
        if User.query.filter(User.username == request.json['username']).count() != 0 or User.query.filter(User.email == request.json['email']).count() != 0:
            return abort(409)

        u = User(request.json['username'], request.json['email'], request.json['salted_password'],
                 request.json['profile_pic'], request.json.get('expiry', '9999-12-31 23:59:59'),
                 request.json.get('token', ''), request.json.get('authorization', False),
                 request.json.get('created_at', datetime.utcnow()))
        db_session.add(u)
        db_session.commit()

        subject = "Confirm your email"

        token = ts.dumps(u.email, salt='email-confirm-key')

        confirm_url = url_for(
            'sign.confirm_email',
            token=token,
            _external=True)

        html = render_template(
            'email/activate.html',
            confirm_url=confirm_url)

        send_email(u.email, subject, html)

        return Response(status='201')

    return abort(400)

@sign_bp.route('/authorize/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(408)

    u = User.query.filter_by(email=email).first()
    if u == None:
        abort(400)

    u.authorization = True
    db_session.add(u)
    db_session.commit()

    return Response(status='200', content_type='text/html')

@sign_bp.route("/in", methods=['POST'])
def load_user_from_header():
    header_auth = request.headers['Authorization'].replace('Basic ', '', 1)
    header_auth = base64.b64decode(header_auth).decode().split(':')
    u = User.query.filter(User.username == header_auth[0]).first()
    if u == None or check_password_hash(u.salted_password, header_auth[1]) == False:
        return abort(401)

    response = Response(status=200, content_type='application/json')
    session['ID'] = 'PHOLASK SESSION'

    return response

@sign_bp.route("/out", methods=['POST'])
def logout():

    return Response(status=204)