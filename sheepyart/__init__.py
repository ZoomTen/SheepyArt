# Global object
from sheepyart import sheepyart

# Endpoints for main page, registration, etc.
from sheepyart.app import routes

# NOTE: model/init: should I put these models onto their own directory?
from sheepyart.app.models import User
from sheepyart.app.models import Art
from sheepyart.app.models import Category
