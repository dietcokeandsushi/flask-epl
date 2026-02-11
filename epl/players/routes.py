from flask import Blueprint, render_template, redirect, url_for, request, flash
from epl.extensions import db
from epl.models import Club, Player

players_bp = Blueprint('players', __name__, template_folder='templates')

@players_bp.route('/')
def index():
  players = db.session.scalars(db.select(Player)).all()
  return render_template('players/index.html',
                         title='Players Page',
                         players=players)

@players_bp.route('/new', methods=['GET', 'POST'])
def new_player():
  clubs = db.session.scalars(db.select(Club)).all()
  if request.method == 'POST':
    name = request.form['name']
    position = request.form['position']
    nationality = request.form['nationality']
    goals = int(request.form['goals'])
    squad_no = int(request.form['squad_no'])
    img = request.form['img']
    club_id = int(request.form['club_id'])

    clean_sheets = None
    if position == "Goalkeeper":
      val = request.form.get('clean_sheets', '0')
      try:
        clean_sheets = int(val)
      except ValueError:
        clean_sheets = 0  

    player = Player(
        name=name,
        position=position,
        nationality=nationality,
        goals=goals,
        squad_no=squad_no,
        img=img,
        club_id=club_id,
        clean_sheets=clean_sheets
    )
    db.session.add(player)
    db.session.commit()
    flash('add new player successfully', 'success')
    return redirect(url_for('players.index'))
  return render_template('players/new_player.html',
                         title='New Player Page',
                         clubs=clubs)

@players_bp.route('/search', methods=['POST'])
def search_player():
  players = []
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
  clubs = db.session.scalars(db.select(Club)).all()
  if request.method == 'POST':
    name = request.form['name']
    position = request.form['position']
    nationality = request.form['nationality']
    goals = int(request.form['goals'])
    squad_no = int(request.form['squad_no'])
    img = request.form['img']
    club_id = int(request.form['club_id'])

    clean_sheets = None 
    if position == "Goalkeeper":
      val = request.form.get('clean_sheets', '0')
      try:
        clean_sheets = int(val)
      except ValueError:
        clean_sheets = 0

    player.name = name
    player.position = position
    player.nationality = nationality
    player.goals = goals
    player.squad_no = squad_no
    player.img = img
    player.club_id = club_id
    player.clean_sheets = clean_sheets

    
    db.session.commit()
    flash('update player successfully', 'success')
    return redirect(url_for('players.index'))

  return render_template('players/update_player.html',
                         title='Update Player Page',
                         player=player,
                         clubs=clubs)