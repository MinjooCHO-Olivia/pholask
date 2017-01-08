from flask import Blueprint

user_bp = Blueprint('user', __name__)


@user_bp.route("/users/<id>", methods=['GET'])
def profile(id):
    pass
