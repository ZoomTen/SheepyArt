'''
    SheepArt route definitions
'''

# Load global definitions
from sheepart.sheepart import app, conf

# Load routes
from sheepart.app.routes.browse import browse
from sheepart.app.routes.register import register
from sheepart.app.routes.search import search
from sheepart.app.routes.login import login, logout, SiteWideLoginForm

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
