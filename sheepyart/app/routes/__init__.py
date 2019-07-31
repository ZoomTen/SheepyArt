'''
    SheepyArt route definitions
'''

# Load global definitions
from sheepyart.sheepyart import app, conf

# Load routes
from sheepyart.app.routes.browse import browse
from sheepyart.app.routes.register import register
from sheepyart.app.routes.search import search
from sheepyart.app.routes.login import login, logout, SiteWideLoginForm
from sheepyart.app.routes.userpage import userpage
from sheepyart.app.routes.upload import upload
from sheepyart.app.routes.art import art

# Load login data
from flask_login import current_user

# ------------------------- View: register endpoints -------------------------

# Register all search categories
@app.context_processor
def quack_all():
    return dict(
        search_categories=conf["search_categories"],
        site_name=conf["site_name"],
        tagline=conf["tagline"],
        userauthed=current_user,
        globallogin=SiteWideLoginForm(),
    )

# Register all routes
app.register_blueprint(browse)
app.register_blueprint(search)
app.register_blueprint(register)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(userpage)
app.register_blueprint(upload)
app.register_blueprint(art)
