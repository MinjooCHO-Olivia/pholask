from flask import Blueprint, abort
from flask import Response
from flask import json
from flask import session
import services.serviceSettings

user_bp = Blueprint('user', __name__)

@user_bp.route("/me", methods=['GET'])
def my_profile():
    if 'uid' in session:
        u = services.serviceSettings.u.findByUid(session['uid'])
        data = json.dumps({"uid": u.uid, "username": u.username, "email": u.email})
        response = Response(status=200, content_type='application/json')
        response.set_data(data)
        return response
    else:
        return abort(401)

@user_bp.route("/<uid>", methods=['GET'])
def profile(uid):
    if services.serviceSettings.u.isValidUid(uid) == False:
        abort(400)
    u = services.serviceSettings.u.findByUid(uid)
    if u == None:
        abort(404)
    data = json.dumps({"uid": u.uid, "username": u.username, "email": u.email})
    response = Response(status=200, content_type='application/json')
    response.set_data(data)
    return response
