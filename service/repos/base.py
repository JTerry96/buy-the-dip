"""Repository base class."""
from flask_sqlalchemy import SQLAlchemy
from service import db

class BaseRepository():
    """Base repository class for all repositories."""

    def __init__(self, db: SQLAlchemy):
        """Instantiate the repository with a db session."""
        self._db = db

    def add(self, model):
        """Add a model to the database."""
        self._db.session.add(model)

    def update(self, model):
        """Update a model in the database."""
        self._db.session.merge(model)

    def delete(self, model):
        """Delete a model from the database."""
        self._db.session.delete(model)

    def commit(self):
        """Commit the database session."""
        self._db.session.commit()
    
    
