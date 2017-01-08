from flask import Blueprint

album_bp = Blueprint('album', __name__)


@album_bp.route("/<id>", methods=['GET'])
def album(id):
    pass
