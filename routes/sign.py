from datetime import datetime
from flask import Blueprint, session, request, url_for, render_template, abort, Flask, Response, json
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import check_password_hash
from wtforms import Form, StringField, PasswordField, validators
from models.user import User
from services.emailService import send_email
import base64
import wtforms_json
import services.serviceSettings

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
        if services.serviceSettings.u.usernameCount(request.json['username']) != 0 or services.serviceSettings.u.emailCount(request.json['email']) != 0:
            return abort(409)

        u = User(request.json['username'], request.json['email'], request.json['salted_password'],
                 request.json['profile_pic'], request.json.get('expiry', '9999-12-31 23:59:59'),
                 token='', authorized=False, created_at=datetime.utcnow())

        services.serviceSettings.u.addUser(u)

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

    u = services.serviceSettings.u.findByEmail(email)

    if u == None:
        abort(400)

    services.serviceSettings.u.giveAuth(u)
    services.serviceSettings.u.addUser(u)

    return Response(status='200', content_type='text/html')

@sign_bp.route("/in", methods=['POST'])
def load_user_from_header():
    header_auth = request.headers['Authorization'].replace('Basic ', '', 1)
    header_auth = base64.b64decode(header_auth).decode().split(':')
    u = services.serviceSettings.u.findByUsername(header_auth[0])

    if u == None or check_password_hash(u.salted_password, header_auth[1]) == False:
        return abort(401)

    session['uid'] = u.uid
    response = Response(status=200, content_type='application/json')
    data = json.dumps({"uid":u.uid, "username": u.username, "email": u.email})
    response.set_data(data)
    return response

@sign_bp.route("/out", methods=['POST'])
def logout():
    if 'uid' in session:
        session.pop('uid', None)
        return Response(status=204)
    else:
        return abort(401)

@sign_bp.route("/leave", methods=['POST'])
def secede():
    if 'uid' in session:
        u = services.serviceSettings.u.findByUid(session['uid'])
        services.serviceSettings.u.deleteUser(u)
        return Response(status=204)
    else:
        abort(status=401)