# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from uuid import uuid4
from odoo.addons.test_http_request.common import mock_odoo_request
from odoo.tests import common
from ..controllers.github import (
    GithubEvent,
    GITHUB_EVENT_TOKEN_PARAM,
    GITHUB_TOKEN_HEADER,
)


class TestPullRequest(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env['github.event'].search([]).unlink()
        cls.token = 'sha1={}'.format(str(uuid4()))
        cls.env['ir.config_parameter'].set_param(GITHUB_EVENT_TOKEN_PARAM, cls.token)

    def setUp(self):
        super().setUp()
        self.controller = GithubEvent()
        self.headers = {GITHUB_TOKEN_HEADER: self.token}
        self.data = {
            "action": "created",
        }

    def _get_created_event(self):
        return self.env['github.event'].search([])

    def test_after_called__event_created(self):
        with mock_odoo_request(self.env, headers=self.headers, data=self.data):
            response = self.controller.new_github_event()

        assert response.status_code == 201
        assert len(self._get_created_event()) == 1

    def test_event_created_with_payload(self):
        with mock_odoo_request(self.env, headers=self.headers, data=self.data):
            self.controller.new_github_event()

        event = self._get_created_event()
        assert event.payload == json.dumps(self.data)

    def test_if_token_not_passed__return_error_401(self):
        del self.headers[GITHUB_TOKEN_HEADER]

        with mock_odoo_request(self.env, headers=self.headers, data=self.data):
            response = self.controller.new_github_event()

        assert response.status_code == 401
        assert not self._get_created_event()

    def test_if_wrong_token_passed__return_error_401(self):
        self.headers[GITHUB_TOKEN_HEADER] = 'sha1={}'.format(str(uuid4()))

        with mock_odoo_request(self.env, headers=self.headers, data=self.data):
            response = self.controller.new_github_event()

        assert response.status_code == 401
        assert not self._get_created_event()
