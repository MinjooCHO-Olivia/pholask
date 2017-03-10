from datetime import datetime
from flask import Blueprint, session, abort, request, Response, json, Flask
from werkzeug.utils import secure_filename
from models.album import Album
from models.album_tag import Album_tag
from models.photo import Photo
import os
import services.serviceSettings

album_bp = Blueprint('album', __name__)

'''리눅스 서버에서 어떻게 돌릴지'''
UPLOAD_FOLDER = 'C:\\Users\\Home\\Documents\\pholask-backend\\image'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@album_bp.route("/", methods=['POST'])
def make_album():
    if 'uid' in session:
        u = services.serviceSettings.u.findByUid(session['uid'])
        if request.json['title'] == "":
            abort(400)
        u.albums = [Album(title=request.json['title'], created_at=datetime.utcnow())]
        services.serviceSettings.u.addUser(u)
        a = services.serviceSettings.a.findByUid(session['uid'])
        for x in range(len(request.json['tag'])):
            a.album_tags.append(Album_tag(request.json['tag'][x]))
            x += 1
        services.serviceSettings.a.addAlbum(a)
        response = Response(status=200, content_type='application/json')
        data = json.dumps({"aid": a.aid, "title": a.title, "createdAt": a.created_at})
        response.set_data(data)
        return response
    else:
        return abort(401)

@album_bp.route("/<aid>", methods=['DELETE'])
def delete_album(aid):
    if 'uid' in session:
        if services.serviceSettings.a.isValidAid(aid) == False:
            abort(401)
        a = services.serviceSettings.a.findByAid(aid)
        if a == None:
            abort(404)
        u = services.serviceSettings.u.findByUid(uid=session['uid'])
        if a.user_uid != u.uid:
            abort(403)
        services.serviceSettings.a.addAlbum(a)
        response = Response(status=204, content_type='application/json')
        return response
    else:
        abort(401)

@album_bp.route("/<aid>/follow", methods=['POST'])
def follow_album(aid):
    if 'uid' in session:
        if services.serviceSettings.a.isValidAid(aid) == False:
            abort(401)
        a = services.serviceSettings.a.findByAid(aid)
        if a == None:
            abort(404)
        follower = services.serviceSettings.u.findByUid(uid=session['uid'])
        if (follower in a.follow) == True:
            abort(409)
        a.follow.append(follower)
        services.serviceSettings.a.addAlbum(a)
        response = Response(status=200, content_type='application/json')
        data = json.dumps({"follow": "true", "count": len(a.follow)})
        response.set_data(data)
        return response
    else:
        abort(401)

@album_bp.route("/<aid>/unfollow", methods=['POST'])
def unfollow_album(aid):
    if 'uid' in session:
        if services.serviceSettings.a.isValidAid(aid) == False:
            abort(401)
        a = services.serviceSettings.a.findByAid(aid)
        if a == None:
            abort(404)
        follower = services.serviceSettings.u.findByUid(uid=session['uid'])
        if (follower in a.follow) != True:
            abort(409)
        a.follow.remove(follower)
        services.serviceSettings.a.addAlbum(a)
        response = Response(status=200, content_type='application/json')
        data = json.dumps({"follow": "false", "count": len(a.follow)})
        response.set_data(data)
        return response
    else:
        abort(401)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@album_bp.route("/<aid>/photos", methods=['POST'])
def photos(aid):
    if 'uid' in session:
        if 'file' not in request.files:
            return abort(401)
        file = request.files['file']
        if file.filename == '':
            return abort(400)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            a = services.serviceSettings.a.findByAid(aid)
            if a == None:
                abort(404)
            if a.user != services.serviceSettings.u.findByUid(session['uid']):
                abort(403)
            a.photos = [Photo(image=app.config['UPLOAD_FOLDER']+filename, content=request.form['content'], created_at=datetime.utcnow())]
            services.serviceSettings.a.addAlbum(a)
            return Response(status=201)
    else:
        abort(401)