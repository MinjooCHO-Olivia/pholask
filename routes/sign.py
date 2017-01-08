from flask import Blueprint

sign_bp = Blueprint('sign', __name__)


@sign_bp.route("/in", methods=['POST'])
def login():
    pass


@sign_bp.route("//out", methods=['POST'])
def logout():
    pass


@sign_bp.route("/up", methods=['POST'])
def enroll():
    pass
