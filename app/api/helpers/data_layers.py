from flask_rest_jsonapi.data_layers.base import BaseDataLayer

from app.api.helpers.db import safe_query
from app.models.geokret import Geokret

GEOKRET_TYPE_TRADITIONAL = "0"
GEOKRET_TYPE_BOOK = "1"
GEOKRET_TYPE_HUMAN = "2"
GEOKRET_TYPE_COIN = "3"
GEOKRET_TYPE_KRETYPOST = "4"

GEOKRET_TYPES_TEXT = {
    GEOKRET_TYPE_TRADITIONAL: "Traditional",
    GEOKRET_TYPE_BOOK: "A book/CD/DVD",
    GEOKRET_TYPE_HUMAN: "A Human",
    GEOKRET_TYPE_COIN: "A coin",
    GEOKRET_TYPE_KRETYPOST: "KretyPost",
}

GEOKRETY_TYPES = [
    {'id': GEOKRET_TYPE_TRADITIONAL, 'name': GEOKRET_TYPES_TEXT[GEOKRET_TYPE_TRADITIONAL]},
    {'id': GEOKRET_TYPE_BOOK, 'name': GEOKRET_TYPES_TEXT[GEOKRET_TYPE_BOOK]},
    {'id': GEOKRET_TYPE_HUMAN, 'name': GEOKRET_TYPES_TEXT[GEOKRET_TYPE_HUMAN]},
    {'id': GEOKRET_TYPE_COIN, 'name': GEOKRET_TYPES_TEXT[GEOKRET_TYPE_COIN]},
    {'id': GEOKRET_TYPE_KRETYPOST, 'name': GEOKRET_TYPES_TEXT[GEOKRET_TYPE_KRETYPOST]},
]

GEOKRETY_TYPES_LIST = [
    GEOKRET_TYPE_TRADITIONAL,
    GEOKRET_TYPE_BOOK,
    GEOKRET_TYPE_HUMAN,
    GEOKRET_TYPE_COIN,
    GEOKRET_TYPE_KRETYPOST,
]

MOVE_TYPE_DROPPED = "0"
MOVE_TYPE_GRABBED = "1"
MOVE_TYPE_COMMENT = "2"
MOVE_TYPE_SEEN = "3"
MOVE_TYPE_ARCHIVED = "4"
MOVE_TYPE_DIPPED = "5"

MOVE_TYPES_TEXT = {
    MOVE_TYPE_DROPPED: 'Dropped to',
    MOVE_TYPE_GRABBED: 'Grabbed from',
    MOVE_TYPE_COMMENT: 'A comment',
    MOVE_TYPE_SEEN: 'Seen in',
    MOVE_TYPE_ARCHIVED: 'Archived',
    MOVE_TYPE_DIPPED: 'Dipped',
}

MOVE_TYPES = [
    {'id': MOVE_TYPE_DROPPED, 'name': MOVE_TYPES_TEXT[MOVE_TYPE_DROPPED]},
    {'id': MOVE_TYPE_GRABBED, 'name': MOVE_TYPES_TEXT[MOVE_TYPE_GRABBED]},
    {'id': MOVE_TYPE_COMMENT, 'name': MOVE_TYPES_TEXT[MOVE_TYPE_COMMENT]},
    {'id': MOVE_TYPE_SEEN, 'name': MOVE_TYPES_TEXT[MOVE_TYPE_SEEN]},
    {'id': MOVE_TYPE_ARCHIVED, 'name': MOVE_TYPES_TEXT[MOVE_TYPE_ARCHIVED]},
    {'id': MOVE_TYPE_DIPPED, 'name': MOVE_TYPES_TEXT[MOVE_TYPE_DIPPED]},
]

MOVE_TYPES_LIST = [
    MOVE_TYPE_DROPPED,
    MOVE_TYPE_GRABBED,
    MOVE_TYPE_COMMENT,
    MOVE_TYPE_SEEN,
    MOVE_TYPE_ARCHIVED,
    MOVE_TYPE_DIPPED,
]
# MOVE_TYPES_COUNT = 6


class GeoKretyTypeDataLayer(BaseDataLayer):

    def get_object(self, view_kwargs, qs=None):
        """Retrieve an object
        :params dict view_kwargs: kwargs from the resource view
        :return DeclarativeMeta: an object
        """
        if 'id' in view_kwargs:
            type_id = view_kwargs['id']
        elif 'geokret_id' in view_kwargs:
            geokret = safe_query(self, Geokret, 'id', view_kwargs['geokret_id'], 'id')
            type_id = int(geokret.type)
        else:  # pragma: no cover
            return None
        try:
            return GEOKRETY_TYPES[type_id]
        except IndexError:
            return None

    def get_collection(self, qs, view_kwargs):
        """Retrieve a collection of objects
        :param QueryStringManager qs: a querystring manager to retrieve information from url
        :param dict view_kwargs: kwargs from the resource view
        :return tuple: the number of object and the list of objects
        """
        return len(GEOKRETY_TYPES), GEOKRETY_TYPES


class MovesTypeDataLayer(BaseDataLayer):

    def get_object(self, view_kwargs):
        """Retrieve an object
        :params dict view_kwargs: kwargs from the resource view
        :return DeclarativeMeta: an object
        """
        try:
            return MOVE_TYPES[view_kwargs['id']]
        except IndexError:
            return None

    def get_collection(self, qs, view_kwargs):
        """Retrieve a collection of objects
        :param QueryStringManager qs: a querystring manager to retrieve information from url
        :param dict view_kwargs: kwargs from the resource view
        :return tuple: the number of object and the list of objects
        """
        return len(MOVE_TYPES_LIST), MOVE_TYPES
