# © 2019 - Today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from odoo import http
from odoo.http import request
from werkzeug.wrappers import Response

import logging
_logger = logging.getLogger(__name__)

GITHUB_EVENT_TOKEN_PARAM = 'github_pull_request.token'
GITHUB_TOKEN_HEADER = 'X-Hub-Signature'


def _get_github_token_from_headers() -> str:
    return request.httprequest.headers.get(GITHUB_TOKEN_HEADER, "")


def _check_github_event_token(token: str) -> bool:
    expected_token = request.env['ir.config_parameter'].sudo().get_param(GITHUB_EVENT_TOKEN_PARAM)
    return expected_token == token


def _get_github_event_payload() -> dict:
    request_data = request.httprequest.data
    return json.loads(request_data.decode())


class GithubEvent(http.Controller):

    @http.route('/web/github/event', type='json', auth='none', sitemap=False)
    def new_github_event(self):
        token = _get_github_token_from_headers()

        if not token:
            _logger.info("A token is required to submit a new event.")
            return Response("A token is required to submit a new event.", status=401)

        if not _check_github_event_token(token):
            _logger.info("The given token is not valid.")
            return Response("The given token is not valid.", status=401)

        request.env['github.event'].sudo().create({
            'payload': json.dumps(_get_github_event_payload()),
        })

        return Response(status=201)
