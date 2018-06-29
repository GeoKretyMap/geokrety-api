# from .celery import celery
import requests

import geopy.distance
from app.models import db
from app.models.move import Move

# @app.task
# def add(x, y):
#     return x + y


def compute_move_distances(geokret_id):
    """ Recompute and update all moves distances for a GeoKret
    """
    moves = Move.query.filter(Move.geokret_id == geokret_id).order_by(Move.moved_on_date_time.asc())

    last = None
    for move in moves:
        if move.latitude is None:
            continue
        if last is None:
            last = move
            continue

        distance = geopy.distance.distance((last.latitude, last.longitude), (move.latitude, move.longitude)).km
        move.distance = int(distance)
        last = move
    db.session.commit()


def update_country_and_altitude(move_id):
    """ Obtain and update country and altitude of a move
    """

    move = Move.query.get(move_id)

    response = requests.get('https://geo.kumy.org/api/getCountry?lat={}&lon={}'.format(move.latitude, move.longitude))
    if response.ok:
        move.country = response.text
    else:
        move.country = 'XYZ'

    response = requests.get('https://geo.kumy.org/api/getElevation?lat={}&lon={}'.format(move.latitude, move.longitude))
    if response.ok:
        move.altitude = response.text
    else:
        move.altitude = '-2000'
