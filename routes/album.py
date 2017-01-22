from flask import Blueprint
from routes.sign import login_required

album_bp = Blueprint('album', __name__)


@album_bp.route("/<id>", methods=['GET'])
@login_required
def album(id):
    pass
