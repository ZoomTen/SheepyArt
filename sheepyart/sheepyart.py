'''
    SheepyArt global object
'''

from os import path

# Base app
# TODO: sheepyart: Try using Quart+Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Login support
from flask_login import LoginManager

# Haml + Sass support
from werkzeug import ImmutableDict

# Migration
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# For the definition file
import json

# Sanitizer
from flask_bleach import Bleach

# Search
from flask_msearch import Search

# URL quote
from urllib.parse import quote_plus

# ------------------------- Definitions -------------------------
with open(path.join("sheepyart", "app", "definitions.json"), "r") as def_files:
    # Load our JSON definition file as a dictionary that
    # we can use
    conf = json.load(def_files)

db_file = conf["db_file"]

base = path.abspath(path.dirname(__file__))

# ------------------------- Control -------------------------


class Hamlisk(Flask):
    "Flask, but with HAMLish"
    jinja_options = ImmutableDict(
        extensions=['jinja2.ext.autoescape',
                    'jinja2.ext.with_',
                    'hamlish_jinja.HamlishExtension']
    )

    def __init__(self):
        Flask.__init__(self, __name__)


app = Hamlisk()

# HAMLish settings
app.jinja_env.hamlish_mode = 'indented'
app.jinja_env.hamlish_enable_div_shortcut = True

# App stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(base, db_file)

app.config['SECRET_KEY'] = conf["secret"]

app.config['MSEARCH_INDEX_NAME'] = 'sheepyart_search'
app.config['MSEARCH_BACKEND'] = 'whoosh'

#app.config['SQLALCHEMY_ECHO'] = True

# Custom filters
app.jinja_env.filters['quote'] = lambda x: quote_plus(x)

# Make db
db = SQLAlchemy(app)

# Migration
migration = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Login manager
logins = LoginManager(app)
logins.login_view = 'login.do_login'
logins.login_message_category = 'info'

# Sanitizer settings
app.config['BLEACH_ALLOWED_TAGS'] = ['a', 'abbr', 'acronym', 'b', 'blockquote',
                                    'code', 'em', 'i', 'li', 'ol', 'strong',
                                    'ul', 'p', 'h1', 'h2', 'h3', 'h4', 'h5',
                                    'h6', 'pre', 'small', 'table', 'thead',
                                    'tbody', 'tfoot', 'th', 'td', 'tr'
                                     ]
app.config['BLEACH_STRIP_MARKUP'] = True

# Default sanitizer. Should there be a need for
# custom sanitizers, routes should import their
# own bleach modules
# Clorox
scrub = Bleach(app)

# Search functions
search = Search(app)


# TODO: sheepyart: use flask-talisman instead for these
@app.after_request
def set_headers(response):
    response.headers['X-Frame-Options'] = 'sameorigin'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
