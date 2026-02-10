from flask import Blueprint, render_template, redirect, url_for, request, flash
from epl.extensions import db
from epl.models import Club

clubs_bp = Blueprint('clubs', __name__, template_folder='templates')

@clubs_bp.route('/')
def index():
    query = db.session.query(Club)
    clubs = db.session.scalars(query).all()
    return render_template('clubs/index.html', 
                            title='Clubs Page', 
                            clubs=clubs)

@clubs_bp.route('/new', methods=['GET', 'POST'])
def new_club():
  if request.method == 'POST':
    name = request.form['name']
    stadium = request.form['stadium']
    year = int(request.form['year'])
    logo = request.form['logo']

    club = Club(name=name, stadium=stadium, year=year, logo=logo)
    db.session.add(club)
    db.session.commit()
    flash('add new club successfully', 'success')
    return redirect(url_for('clubs.index'))
  
  return render_template('clubs/new_club.html',
                         title='New Club Page')

@clubs_bp.route('/clubs/search', methods=['GET', 'POST'])
def search_club():
  club_name = request.form['club_name']
  club = db.session.scalars(db.select(Club).where(Club.name.like(f'%{club_name}%'))).all()
  return render_template('clubs/search_club.html',
                  title='Search Club Page',
                  clubs=club)

@clubs_bp.route('/<int:id>/info')
def info_club(id):
  clube = db.session.get(Club, id)
  return render_template('clubs/info_club.html',
                         title='Club Info Page',
                         club=clube)        

@clubs_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_club(id):
  club = db.session.get(Club, id)
  if request.method == 'POST':
    name = request.form['name']
    stadium = request.form['stadium']
    year = int(request.form['year'])
    logo = request.form['logo']
    club.name = name
    club.stadium = stadium
    club.year = year
    club.logo = logo
    db.session.add(club)
    db.session.commit()
    flash('update club successfully', 'success')
    return redirect(url_for('all_clubs'))
  return render_template('clubs/update_club.html',
                         title='Update Club Page',
                         club=club)