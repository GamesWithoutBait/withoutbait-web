from app import Blueprint


bp = Blueprint(__name__)

from . import errors, game, list_games, login, user
