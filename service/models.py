"""
Account Model
"""
import logging
from datetime import date
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")
db = SQLAlchemy()


class PersistentBase:
    """Base class for persistence"""
    def __init__(self):
        self.id = None

    def create(self):
        logger.info("Creating %s", self.name)
        db.session.add(self)
        db.session.commit()

    def update(self):
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        logger.info("Initializing database")
        cls.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        logger.info("Processing all %s", cls.__name__)
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)


class Account(db.Model, PersistentBase):
    """Class that represents an Account"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32))
    date_joined = db.Column(db.Date(), nullable=False, default=date.today())

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": str(self.date_joined),
        }

    def deserialize(self, data):
        self.name = data["name"]
        self.email = data["email"]
        self.address = data.get("address")
        self.phone_number = data.get("phone_number")
        if "date_joined" in data:
            self.date_joined = date.fromisoformat(data["date_joined"])
        return self
