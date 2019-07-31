from datetime import datetime, date
from sheepyart.sheepyart import db, logins
from flask_login import UserMixin

# ------------------------- Interfacing -------------------------

@logins.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# ------------------------- Model -------------------------

class User(db.Model, UserMixin):
    '''
    Required fields:
        username(String, 16, unique)
        dispname(String, 64)
        email(String, 128, unique)
        password(String, 60, hashed)
        dob(Date)
        gender(Integer)
        country(Integer)
    Optional fields:
        avatar(String, 128)
    Other fields:
        art(db, Art)
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    dispname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    # FIXME: Proper classification for gender and country?
    gender = db.Column(db.Integer, nullable=False)
    country = db.Column(db.Integer, nullable=False)
    # avatar is a static image link
    avatar = db.Column(db.String(128), nullable=False, default='default.jpg')
    art = db.relationship('Art', backref='by', lazy=True)

    def __repr__(self):
        return 'User(' + str(self.username) + ', ' + str(self.email) + ', ' + str(self.avatar) +')'

class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    # image is a static image link
    image = db.Column(db.String(128), nullable=False, default='art.jpg')
    # thumbnail is a static image link, default='default.jpg'
    thumbnail = db.Column(db.String(128), nullable=False, default='thumb.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorites = db.Column(db.Integer, nullable=False, default=0)
    views = db.Column(db.Integer, nullable=False, default=0)
    pubdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False, default='')
    tags = db.Column(db.String(256), nullable=False, default='')
    category = db.Column(db.Integer, nullable=False, default=0)
    nsfw = db.Column(db.Integer, nullable=False, default=0)
    license = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return 'Art(' + str(self.title) + ', ' + str(self.image) + ', ' + str(self.category) + ', ' + str(self.favorites) + ', ' + str(self.views) + ', ' + str(self.pubdate) + ')'
