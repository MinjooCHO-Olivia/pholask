from flask import Flask
from resources.database import db_session, init_db
from routes.album import album_bp
from routes.photo import photo_bp
from routes.sign import sign_bp
from routes.user import user_bp


app = Flask(__name__)

app.register_blueprint(album_bp, url_prefix="/albums")
app.register_blueprint(photo_bp, url_prefix="/photos")
app.register_blueprint(sign_bp, url_prefix="/sign")
app.register_blueprint(user_bp, url_prefix="/users")

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    init_db()
    app.run()
