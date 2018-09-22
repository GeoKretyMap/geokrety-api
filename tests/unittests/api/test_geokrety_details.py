# -*- coding: utf-8 -*-

import urllib

from flask_rest_jsonapi.exceptions import ObjectNotFound
from parameterized import parameterized

from app import current_app as app
from app.api.helpers.data_layers import (GEOKRET_TYPE_BOOK, GEOKRET_TYPE_COIN,
                                         GEOKRET_TYPE_HUMAN,
                                         GEOKRET_TYPE_KRETYPOST,
                                         GEOKRET_TYPE_TRADITIONAL,
                                         MOVE_TYPE_ARCHIVED, MOVE_TYPE_COMMENT,
                                         MOVE_TYPE_DIPPED, MOVE_TYPE_DROPPED,
                                         MOVE_TYPE_GRABBED, MOVE_TYPE_SEEN,
                                         MOVE_TYPES_TEXT)
from app.api.helpers.db import safe_query
from app.models.move import Move
from tests.unittests.utils.base_test_case import (BaseTestCase, request_context,
                                                  custom_name_geokrety_move_type)
from tests.unittests.utils.payload.geokret import GeokretyPayload
from tests.unittests.utils.responses.geokret import GeokretResponse
from tests.unittests.utils.static_test_cases import (EMPTY_TEST_CASES,
                                                     HTML_SUBSET_TEST_CASES,
                                                     NO_HTML_TEST_CASES,
                                                     UTF8_TEST_CASES)


class TestGeokretDetails(BaseTestCase):
    """Test Geokrety details"""

    def send_get(self, id, args=None, **kwargs):
        args_ = '' if args is None else urllib.urlencode(args)
        url = "/v1/geokrety/%s?%s" % (id, args_)
        return GeokretResponse(self._send_get(url, **kwargs).get_json())

    # has_normal_attributes

    @request_context
    def test_geokret_details_has_normal_attributes_as_anonymous_user(self):
        geokret = self.blend_geokret()
        response = self.send_get(geokret.id)
        response.assertHasPublicAttributes(geokret)
        with self.assertRaises(AssertionError):
            response.assertHasRelationshipOwnerData(geokret.owner_id)
        with self.assertRaises(AssertionError):
            response.assertHasRelationshipHolderData(geokret.holder_id)

    @request_context
    def test_geokret_details_has_normal_attributes_as_authenticated_user(self):
        geokret = self.blend_geokret()
        response = self.send_get(geokret.id, user=self.user_1)
        response.assertHasPublicAttributes(geokret)
        with self.assertRaises(AssertionError):
            response.assertHasRelationshipOwnerData(geokret.owner_id)
        with self.assertRaises(AssertionError):
            response.assertHasRelationshipHolderData(geokret.holder_id)

    @request_context
    def test_geokret_details_has_normal_attributes_as_admin_user(self):
        geokret = self.blend_geokret()
        response = self.send_get(geokret.id, user=self.admin)
        response.assertHasPublicAttributes(geokret)
        with self.assertRaises(AssertionError):
            response.assertHasRelationshipOwnerData(geokret.owner_id)
        with self.assertRaises(AssertionError):
            response.assertHasRelationshipHolderData(geokret.holder_id)

    # has_tracking_code

    @request_context
    def test_geokret_details_has_tracking_code_as_anonymous_user(self):
        geokret = self.blend_geokret()
        response = self.send_get(geokret.id, user=None)
        response.assertHasTrackingCode(None)

    @request_context
    def test_geokret_details_has_tracking_code_as_authenticated_user(self):
        geokret = self.blend_geokret(owner=self.admin)
        response = self.send_get(geokret.id, user=self.user_1)
        response.assertHasTrackingCode(None)

    @request_context
    def test_geokret_details_has_tracking_code_as_admin_user(self):
        geokret = self.blend_geokret(owner=self.user_1)
        response = self.send_get(geokret.id, user=self.admin)
        response.assertHasTrackingCode(geokret.tracking_code)

    @request_context
    def test_geokret_details_has_tracking_code_as_owner(self):
        geokret = self.blend_geokret(owner=self.user_1)
        response = self.send_get(geokret.id, user=self.user_1)
        response.assertHasTrackingCode(geokret.tracking_code)

    @request_context
    def test_geokret_details_has_tracking_code_as_holder(self):
        geokret = self.blend_geokret(holder=self.user_1)
        response = self.send_get(geokret.id, user=self.user_1)
        response.assertHasTrackingCode(geokret.tracking_code)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED, True],
        [MOVE_TYPE_GRABBED, True],
        [MOVE_TYPE_COMMENT, False],
        [MOVE_TYPE_SEEN, True],
        [MOVE_TYPE_ARCHIVED, True],
        [MOVE_TYPE_DIPPED, True],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_geokret_details_has_tracking_code_when_user_has_touched(self, input, expected):
        geokret = self.blend_geokret(created_on_datetime="2018-09-18T23:37:01")
        self.blend_move(geokret=geokret, author=self.user_1, move_type_id=input, moved_on_datetime="2018-09-18T23:37:02")
        self.blend_move(geokret=geokret, author=self.user_2, move_type_id=MOVE_TYPE_GRABBED,
                        moved_on_datetime="2018-09-18T23:37:03")
        response = self.send_get(geokret.id, user=self.user_1)
        if expected:
            response.assertHasTrackingCode(geokret.tracking_code)
        else:
            response.assertHasTrackingCode(None)

    # sparse_fieldset

    @request_context
    def test_geokret_details_sparse_fieldset(self):
        geokret = self.blend_geokret(owner=self.user_1)
        response = self.send_get(geokret.id, args={'fields[geokret]': 'name,description'})
        response.assertHasAttribute('name', geokret.name)
        response.assertHasAttribute('description', geokret.description)
        with self.assertRaises(AssertionError):
            assert response.get_attribute('missing')

    @parameterized.expand([
        [None, False],
        ['admin', True],
        ['user_1', True],  # Owner
        ['user_2', False],
    ])
    @request_context
    def test_geokret_details_sparse_fieldset_has_tracking_code(self, input, expected):
        geokret = self.blend_geokret(owner=self.user_1)
        response = self.send_get(geokret.id, user=getattr(self, input) if input else None, args={'fields[geokret]': 'tracking_code'})
        response.pprint()
        if expected:
            response.assertHasTrackingCode(geokret.tracking_code)
        else:
            response.assertHasTrackingCode(None)

    @parameterized.expand([
        [MOVE_TYPE_DROPPED, True],
        [MOVE_TYPE_GRABBED, True],
        [MOVE_TYPE_COMMENT, False],
        [MOVE_TYPE_SEEN, True],
        [MOVE_TYPE_ARCHIVED, True],
        [MOVE_TYPE_DIPPED, True],
    ], doc_func=custom_name_geokrety_move_type)
    @request_context
    def test_geokret_details_sparse_fieldset_has_tracking_code_when_user_has_touched(self, input, expected):
        geokret = self.blend_geokret(created_on_datetime="2018-09-20T23:15:30")
        self.blend_move(geokret=geokret, author=self.user_1, move_type_id=input,
                        moved_on_datetime="2018-09-20T23:15:31")
        self.blend_move(geokret=geokret, author=self.user_2, move_type_id=MOVE_TYPE_GRABBED,
                        moved_on_datetime="2018-09-20T23:15:32")
        response = self.send_get(geokret.id, user=self.user_1, args={'fields[geokret]': 'tracking_code'})
        if expected:
            response.assertHasTrackingCode(geokret.tracking_code)
        else:
            response.assertHasTrackingCode(None)

    # has_relationships

    @request_context
    def test_geokret_details_has_relationships_owner_data(self):
        geokret = self.blend_geokret(owner=self.user_1)
        response = self.send_get(geokret.id, user=None)
        response.assertHasRelationshipOwnerData(geokret.owner_id)

    @request_context
    def test_geokret_details_has_relationships_holder_data(self):
        geokret = self.blend_geokret(holder=self.user_2)
        response = self.send_get(geokret.id, user=None)
        response.assertHasRelationshipHolderData(geokret.holder_id)

    # @request_context
    # def test_geokret_details_has_relationships_avatar_data(self):
    #     # TODO
    #     pass

    # @request_context
    # def test_geokret_details_has_relationships_all_pictures_data(self):
    #     # TODO
    #     pass

    # @request_context
    # def test_geokret_details_has_relationships_last_position_data(self):
    #     # TODO
    #     pass

    # @request_context
    # def test_geokret_details_has_relationships_last_log_data(self):
    #     # TODO
    #     pass

    @request_context
    def test_geokret_details_has_relationships_moves_data(self):
        geokret = self.blend_geokret()
        moves = self.blend_move(count=5, geokret=geokret, author=self.user_1, move_type_id=MOVE_TYPE_GRABBED)
        moves_ids = [move.id for move in moves]
        response = self.send_get(geokret.id, user=self.user_1, args={'include': 'moves'})
        response.assertHasRelationshipMovesData(moves_ids)