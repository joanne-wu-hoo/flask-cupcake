""" Models for Cupcake app """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE = 'https://tinyurl.com/truffle-cupcake'


def connect_db(app):
    """ Connect to database """
    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """ Cupcake """

    __tablename__ = "cupcakes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
        )
    flavor = db.Column(
        db.String(30),
        nullable=False
        )
    size = db.Column(
        db.String(20),
        nullable=False
        )
    rating = db.Column(
        db.Float,
        nullable=False
        )
    image = db.Column(
        db.String,
        nullable=False,
        default=DEFAULT_IMAGE
        )

    def serialize(self):
        """ Return a dictionary of data """
        serialized_cupcake = dict(
            id=self.id,
            flavor=self.flavor,
            size=self.size,
            rating=self.rating,
            image=self.image,
        )
        return serialized_cupcake

    def __repr__(self):
        return f'<Cupcake {self.id} {self.flavor} {self.size}>'