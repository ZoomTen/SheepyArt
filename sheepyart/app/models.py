"""SheepyArt models / tables for the database"""

from datetime import datetime
from sheepyart.sheepyart import db, logins
from flask_login import UserMixin

# ------------------------- Interfacing -------------------------

@logins.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# ------------------------- Model -------------------------

class User(db.Model, UserMixin):
    """User column.

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
        joindate(Date)
    Other fields:
        art(db, Art)
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    dispname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    joindate = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    # NOTE: model/user: should I need a table for genders and countries?
    gender = db.Column(db.Integer, nullable=False)
    country = db.Column(db.Integer, nullable=False)
    # avatar is a static image link
    avatar = db.Column(db.String(128), nullable=False, default='default.jpg')
    art = db.relationship('Art', backref='by', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avatar}')"


class Art(db.Model):
    """Art column.

    Required fields:
        title(String, 128)
    Optional fields:
        image(String, 128)      -> relative to static/uploads/
        thumbnail(String, 128)  -> relative to static/thumbnail/
        user_id(Integer)
        favorites(Integer)      -> requires user login to favorite
        views(Integer)          -> should be updated every time the page is
                                   viewed BY unique IDs
        pubdate(DateTime)
        description(Text)       -> indexable
        tags(String, 256)       -> space separated
        category(Integer)       -> must point to a valid category
        nsfw(Integer)           -> must be between 0:none, 1:mild, 2:explicit
        license(Integer)
    """
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
        return f"Art('{self.title}', '{self.image}', cat:{self.category})"


class Category(db.Model):
    """Category column.

    Required fields:
        title(String, 128)
    Optional fields:
        parent_id(Integer, nullable)
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    parent_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Category('{self.title}', parent:{self.parent_id})"


# NOTE: models: this "licenses" table may or may not be here to stay.
class License(db.Model):
    """License column.

    Required fields:
        title(String, 128)
    Optional fields:
        commercial_allowed(Boolean, default=False)
        attrib_required(Boolean, default=False)
        link(String, 128, nullable)
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    commercial_allowed = db.Column(db.Boolean, nullable=False, default=False)
    attrib_required = db.Column(db.Boolean, nullable=False, default=False)
    link = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return f"License('{self.title}', commercial:{self.commercial_allowed}, attrib:{self.attrib_required})"
