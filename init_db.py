from app import app
from app.models import db

# Create an application context
with app.app_context():
    db.create_all()