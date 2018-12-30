

from flask import request
from flask_jwt import current_identity
from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)
from flask_rest_jsonapi.exceptions import ObjectNotFound

from app.api.bootstrap import api
from app.api.helpers.data_layers import GEOKRETY_TYPES_LIST
from app.api.helpers.db import safe_query
from app.api.helpers.exceptions import UnprocessableEntity
from app.api.helpers.permission_manager import has_access
from app.api.helpers.utilities import require_relationship
from app.api.schema.geokrety import GeokretSchemaCreate, GeokretSchemaPublic
from app.models import db
from app.models.geokret import Geokret
from app.models.user import User


class GeokretList(ResourceList):

    def query(self, view_kwargs):
        """Filter geokrety"""
        query_ = self.session.query(Geokret)

        # /users/<int:owner_id>/geokrety-owned
        if view_kwargs.get('owner_id') is not None:
            safe_query(self, User, 'id', view_kwargs['owner_id'], 'owner_id')
            query_ = query_.filter_by(owner_id=view_kwargs['owner_id'])

        # /users/<int:holder_id>/geokrety-held
        if view_kwargs.get('holder_id') is not None:
            safe_query(self, User, 'id', view_kwargs['holder_id'], 'holder_id')
            query_ = query_.filter_by(holder_id=view_kwargs['holder_id'])

        # /geokrety-types/<int:geokrety_type_id>/geokrety
        if view_kwargs.get('geokrety_type_id') is not None:
            if str(view_kwargs['geokrety_type_id']) not in GEOKRETY_TYPES_LIST:
                raise ObjectNotFound(u"{}: {} not found".format('GeokretyType', view_kwargs['geokrety_type_id']), {
                                     u'pointer': '{}'.format('geokrety_type_id')})
            query_ = query_.filter_by(type=str(view_kwargs['geokrety_type_id']))

        return query_

    def post(self, *args, **kwargs):
        self.schema = GeokretSchemaCreate
        return super(GeokretList, self).post(args, kwargs)

    def before_post(self, args, kwargs, data=None):
        # Enforce owner to current user
        if not current_identity.is_admin or 'owner' not in data:
            data['owner'] = current_identity.id

        require_relationship(['type'], data)

        # Enforce holder to owner
        data['holder'] = data['owner']

        if 'born_at_home' in data and data['born_at_home']:
            del data['born_at_home']

    schema = GeokretSchemaPublic
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    decorators = (
        api.has_permission('auth_required', methods="POST"),
    )
    data_layer = {
        'session': db.session,
        'model': Geokret,
        'methods': {
            'query': query,
        },
    }


class GeokretInACacheList(GeokretList):

    def query(self, view_kwargs):
        """Filter geokrety"""
        query_ = self.session.query(Geokret)

        waypoint = request.args.get('waypoint')
        if waypoint:
            return query_.filter_by(last_position__waypoint=waypoint)

        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        if latitude and longitude:
            return query_\
                .filter_by(last_position__latitude=latitude)\
                .filter_by(last_position__latitude=latitude)

        raise UnprocessableEntity("Waypoint or latitude/longitude missing from arguments",
                                  {'pointer': 'args: waypoint or latitude and longitude'})


class GeokretDetail(ResourceDetail):
    def before_patch(self, args, kwargs, data=None):
        data.pop('holder', None)
        data.pop('moves', None)

        if not has_access('is_admin'):
            data.pop('owner', None)

    decorators = (
        api.has_permission('is_geokret_owner', methods="PATCH,DELETE",
                           fetch="id", fetch_as="geokret_id",
                           model=Geokret, fetch_key_url="id"),
    )
    methods = ('GET', 'PATCH', 'DELETE')
    schema = GeokretSchemaPublic
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    data_layer = {
        'session': db.session,
        'model': Geokret,
    }


class GeokretRelationship(ResourceRelationship):
    methods = ['GET']
    schema = GeokretSchemaPublic
    get_schema_kwargs = {'context': {'current_identity': current_identity}}
    data_layer = {
        'session': db.session,
        'model': Geokret,
    }
