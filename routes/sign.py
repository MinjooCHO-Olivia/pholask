from datetime import datetime
import wtforms_json
from flask import Blueprint, session, request, redirect, url_for, flash, render_template, abort, Flask
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import check_password_hash
from wtforms import Form, StringField, PasswordField, validators
from models.user import User
from resources.database import db_session
from resources.email_confirmation import send_email
from functools import wraps

sign_bp = Blueprint('sign', __name__)

app =Flask(__name__)

app.config.update(SECRET_KEY='WFVE#G!voP%m')
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user', None) is None:
            return redirect(
            url_for('sign.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

wtforms_json.init()

class RegistrationForm(Form):
    username = StringField('username', [validators.Length(min=3, max=25)])
    email = StringField('email', [validators.Email(), validators.Length(min=6, max=35)])
    salted_password = PasswordField('salted_password', [validators.DataRequired(), validators.Length(min=6, max=15)])

@sign_bp.route("/up", methods=['POST'])
def enroll():
    form = RegistrationForm.from_json(request.json)
    if form.validate():
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

        return "Sign up ok"

    return "The form is not vaild"

@sign_bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    u = User.query.filter_by(email=email).first()
    """email 없으면 에러보내기"""
    u.authorization = True

    db_session.add(u)
    db_session.commit()

    return "Confirm ok"

@sign_bp.route("/in", methods=['POST'])
def login():
    email = request.json['email']
    salted_password = request.json['salted_password']
    registered_user = User.query.filter_by(email=email).first()
    if registered_user is None:
        flash('Username is invalid', 'error')
        return redirect(url_for('.login'))
    if check_password_hash(registered_user.salted_password, salted_password) != True:
        flash('Password is invalid', 'error')
        return redirect(url_for('.login'))
    return "Login ok"

@sign_bp.route("/out", methods=['POST'])
def logout():
    pass
