from flask import Blueprint
from routes.sign import login_required

user_bp = Blueprint('user', __name__)


@user_bp.route("/users/<id>", methods=['GET'])
@login_required
def profile(id):
    pass
