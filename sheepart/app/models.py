from datetime import datetime
from sheepart import db
# ------------------------- Model -------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    # avatar is a static image link
    avatar = db.Column(db.String(128), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    art = db.relationship('Art', backref='by', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avatar}')"

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

    def __repr__(self):
        return f"Art('{self.title}', '{self.image}', '{self.category}', '{self.favorites}', '{self.views}', '{self.pubdate}')"
