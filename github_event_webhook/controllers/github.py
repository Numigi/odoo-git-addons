# Copyright 2023 - Today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import hmac
import hashlib
import logging
from urllib.parse import urlencode  # <-- Odoo 18 : On utilise la librairie standard

from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

GITHUB_EVENT_SECRET_PARAM = "github_pull_request.github_secret"
GITHUB_SIGNATURE_HEADER = "X-Hub-Signature"


def make_github_signature(request_body: str, secret: str) -> str:
    """Make a Github signature from the given request body and secret."""
    digest = hmac.new(secret.encode(), request_body.encode(), hashlib.sha1).hexdigest()
    return "sha1={}".format(digest)


def _get_github_signature_from_headers() -> str:
    return request.httprequest.headers.get(GITHUB_SIGNATURE_HEADER, "")


def _check_github_event_signature(signature: str) -> bool:
    request_body = urlencode(request.httprequest.form)
    # Odoo 18 : Remplacement de with_user(SUPERUSER_ID) par sudo()
    secret = (
        request.env["ir.config_parameter"]
        .sudo()
        .get_param(GITHUB_EVENT_SECRET_PARAM)
    )
    return make_github_signature(request_body, secret) == signature


class GithubEvent(http.Controller):
    @http.route(
        "/web/github/event", type="http", auth="none", sitemap=False, csrf=False
    )
    def new_github_event(self, **data):
        signature = _get_github_signature_from_headers()

        if not signature:
            message = "The github signature is required to submit a new event."
            _logger.info(message)
            return Response(message, status=401)

        if not _check_github_event_signature(signature):
            message = "The given github signature is not valid."
            _logger.info(message)
            return Response(message, status=401)

        json_payload = self._get_json_payload(data)
        event = self._create_event(json_payload)

        # S'assure que queue_job est bien installé en V18 pour utiliser with_delay()
        event.with_delay().process_job()

        return Response(status=201)

    @staticmethod
    def _get_json_payload(data):
        return data["payload"]

    @staticmethod
    def _create_event(json_payload):
        return (
            request.env["github.event"]
            .sudo()
            .create(
                {
                    "payload": json_payload,
                }
            )
        )
