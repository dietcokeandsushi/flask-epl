from flask import Blueprint, render_template, redirect, url_for, request, flash
from epl.extensions import db
from epl.models import Player, Club

players_bp = Blueprint('players', __name__, template_folder='templates')

@players_bp.route('/')
def index():
  players = db.session.scalars(db.select(Player)).all()
  return render_template('players/index.html',
                         title='Players Page',
                         players=players)

@players_bp.route('/new', methods=['GET', 'POST'])
def new_player():
  club = db.session.scalars(db.select(Club)).all()
  if request.method == 'POST':
    name = request.form['name']
    position = request.form['position']
    Nationality = request.form['nationality']
    goals = int(request.form['goals'])
    squad_no = int(request.form['squad_no'])
    img = request.form['img']
    club_id = int(request.form['club_id'])

    player = Player(name=name, position=position, Nationality=Nationality, goals=goals, squad_no=squad_no, img=img, club_id=club_id)
    db.session.add(player)
    db.session.commit()
    flash('add new player successfully', 'success')
    return redirect(url_for('players.index'))
  return render_template('players/new_player.html',
                         title='New Player Page'
                         , clubs=club)

@players_bp.route('/players/search', methods=['GET', 'POST'])
def search_player():
  if request.method == 'POST':
    player_name = request.form['player_name']
    players = db.session.scalars(db.select(Player).where(Player.name.like(f'%{player_name}%'))).all()
  return render_template('players/search_player.html',
                  title='Search Player Page',
                  players=players)

@players_bp.route('/<int:id>/info')
def info_player(id):                  
  player = db.session.get(Player, id)
  return render_template('players/info_player.html',
                         title='Info Player Page',
                         player=player)


@players_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_player(id):
  player = db.session.get(Player, id)
  query = db.session.query(Club)
  clubs = db.session.scalars(query).all()
  if request.method == 'POST':
    name = request.form['name']
    position = request.form['position']
    Nationality = request.form['nationality']
    goals = int(request.form['goals'])
    squad_no = int(request.form['squad_no'])
    img = request.form['img']
    club_id = int(request.form['club_id'])

    player.name = name
    player.position = position
    player.Nationality = Nationality
    player.goals = goals
    player.squad_no = squad_no
    player.img = img
    player.club_id = club_id

    db.session.add(player)
    db.session.commit()
    flash('update player successfully', 'success')
    return redirect(url_for('players.index'))

  return render_template('players/update_player.html',
                         title='Update Player Page',
                         player=player,
                         clubs=clubs)