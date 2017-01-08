from flask import Blueprint

photo_bp = Blueprint('photo', __name__)


@photo_bp.route("/<id>", methods=['GET'])
def photo(id):
    pass
