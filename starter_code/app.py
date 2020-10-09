#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
  Flask, render_template, request, Response, flash, redirect, url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate
import dateutil.parser
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
db.init_app(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] =  SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue. 
  cities_states = []
  areas = []
  for venue in Venue.query.distinct(Venue.city, Venue.state):
        cities_states.append({"city": venue.city, "state":venue.state})
  for city in cities_states:
        venue_in_area = []
        for area in Venue.query.filter_by(city=city['city']).filter_by(state=city['state']):
              venue_in_area.append({
                "id": area.id,
                "name":area.name,
                "num_upcoming_shows": len(Show.query.filter_by(venue_id=area.id).filter(Show.start_time>datetime.now()).all())
              })
        areas.append({
          "city": city['city'],
          "state": city['state'],
          "venues": venue_in_area
        })       
  return render_template('pages/venues.html', areas=areas);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. // Done
  # seach for Hop should return "The Musical Hop". //Done
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee" //Done
  result = []
  fieldValue = "%{}%".format(request.form["search_term"])
  venues = Venue.query.filter(Venue.name.ilike(fieldValue)).all()  
  for venue in venues:
        result.append({
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": 0,
        })
  data = {
    "count": Venue.query.filter(Venue.name.ilike(fieldValue)).count(),
    "data":result
  }
  return render_template('pages/search_venues.html', results=data, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id //Done
  venue_query = Venue.query.filter_by(id=venue_id).first()
  venue_shows = Show.query.filter_by(venue_id=venue_id).join(Venue).join(Artist).all()            
  upcoming_shows=[]
  past_shows=[]
  upcoming_shows_count = 0
  past_shows_count = 0
  for show in venue_shows:
        if(show.start_time<datetime.now()):
              past_shows_count+=1
              past_shows.append({
                "artist_id": show.artists.id,
                "artist_name": show.artists.name,
                "artist_image_link": show.artists.image_link,
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
              })
        if(show.start_time>datetime.now()):
              upcoming_shows_count+=1
              upcoming_shows.append({
                "artist_id": show.artists.id,
                "artist_name": show.artists.name,
                "artist_image_link": show.artists.image_link,
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
              })
              
  data={
    "id": venue_query.id,
    "name": venue_query.name,
    "genres": venue_query.genres,
    "address": venue_query.address,
    "city": venue_query.city,
    "state": venue_query.state,
    "phone": venue_query.phone,
    "website": venue_query.website,
    "facebook_link": venue_query.facebook_link,
    "seeking_talent": False,
    "image_link": venue_query.image_link,
    "upcoming_shows": upcoming_shows,
    "past_shows": past_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }
  print(Venue.query.filter_by(id=venue_id).order_by('id').first())
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    facebook_link = request.form.get('facebook_link')
    genres = request.form.get('genres')
    venue = Venue(name=name, city=city, state=state,address=address,phone=phone,image_link=image_link, facebook_link=facebook_link, genres=genres)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    # flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database //Done
  data = []
  for artist in Artist.query.all():
        data.append({
          "id": artist.id,
          "name": artist.name
        })
  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. // Done
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band". //Done
  # search for "band" should return "The Wild Sax Band". //Done
  result = []
  fieldValue = "%{}%".format(request.form["search_term"])
  artists = Artist.query.filter(Artist.name.ilike(fieldValue)).all()  
  for artist in artists:
        result.append({
          "id": artist.id,
          "name": artist.name,
          "num_upcoming_shows": len(Show.query.filter_by(artist_id=artist.id).join(Venue).join(Artist).all()),
        })
  data = {
    "count": Artist.query.filter(Artist.name.ilike(fieldValue)).count(),
    "data":result
  }
  return render_template('pages/search_artists.html', results=data, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id //Done
  # TODO: replace with real venue data from the venues table, using venue_id //Done
  artist_query = Artist.query.filter_by(id=artist_id).first()
  artist_shows = Show.query.filter_by(artist_id=artist_id).join(Venue).join(Artist).all()            
  upcoming_shows=[]
  past_shows=[]
  upcoming_shows_count = 0
  past_shows_count = 0
  for show in artist_shows:
        if(show.start_time<datetime.now()):
              past_shows_count+=1
              past_shows.append({
                "vanue_id": show.venues.id,
                "venue_name": show.venues.name,
                "venues_image_link": show.venues.image_link,
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
              })
        if(show.start_time>datetime.now()):
              upcoming_shows_count+=1
              upcoming_shows.append({
                "venue_id": show.venues.id,
                "venue_name": show.venues.name,
                "venue_image_link": show.venues.image_link,
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
              })
              
  data={
    "id": artist_query.id,
    "name": artist_query.name,
    "genres": artist_query.genres,
    "city": artist_query.city,
    "state": artist_query.state,
    "phone": artist_query.phone,
    "website": artist_query.website,
    "facebook_link": artist_query.facebook_link,
    "seeking_talent": False,
    "image_link": artist_query.image_link,
    "upcoming_shows": upcoming_shows,
    "past_shows": past_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id> // Done
  return render_template('forms/edit_artist.html', form=form, artist=Artist.query.filter_by(id=artist_id).first())

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing  // Done
  # artist record with ID <artist_id> using the new attributes // Done
  artist = Artist.query.filter_by(id=artist_id).first()
  artist.name = request.form['name']
  artist.city= request.form['city']
  artist.state = request.form['state']
  artist.phone = request.form['phone']
  artist.genres = request.form['genres']
  artist.facebook_link = request.form['facebook_link']
  db.session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id> // Done
  return render_template('forms/edit_venue.html', form=form, venue=Venue.query.filter_by(id=venue_id).first())

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing // done
  # venue record with ID <venue_id> using the new attributes // done
  venue = Venue.query.filter_by(id=venue_id).first()
  venue.name = request.form['name']
  venue.city= request.form['city']
  venue.state = request.form['state']
  venue.phone = request.form['phone']
  venue.genres = request.form['genres']
  venue.facebook_link = request.form['facebook_link']
  venue.address = request.form['address']
  db.session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    genres = request.form.get('genres')
    website = request.form.get('website')
    image_link = request.form.get('image_link')
    facebook_link = request.form.get('facebook_link')
    seeking_description = request.form.get('seeking_description')
    artist = Artist(name=name, city=city, state=state,phone=phone,genres=genres,website=website,image_link=image_link, facebook_link=facebook_link, seeking_description=seeking_description)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    # flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows // done
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.join(Artist).join(Venue).all()
  showsList = []
  for show in shows:
        showsList.append({
           "venue_id": show.venue_id,
           "venue_name": show.venues.name,
           "artist_id": show.artist_id,
           "artist_name": show.artists.name,
           "artist_image_link": show.artists.image_link,
           "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })
  return render_template('pages/shows.html', shows=showsList)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
      artist_id = request.form.get('artist_id')
      venue_id = request.form.get('venue_id')
      start_time = request.form.get('start_time')
      show = Show(artist_id=artist_id, venue_id=venue_id,start_time=start_time)
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    except:
      db.session.rollback()
    finally:
      db.session.close()
      
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
