from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    website = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    shows = db.relationship('Show', backref='venues', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate \\ Done

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    image_link = db.Column(db.String(500))
    seeking_description = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artists', lazy=True)
    
class Show(db.Model):
    __tablename__ = 'shows'
     
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
            return f'<Show artist_id: {self.artist_id}, venue_id:{self.venue_id}, start_time: {self.start_time}>'
    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate \\ Done

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. \\ Done
