from flask import Blueprint
from routes.sign import login_required

photo_bp = Blueprint('photo', __name__)


@photo_bp.route("/<id>", methods=['GET'])
@login_required
def photo(id):
    pass
