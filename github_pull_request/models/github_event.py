# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import dateutil.parser
import json
from odoo import api, fields, models, _
from odoo.addons.base_sparse_field.models.fields import Serialized
from odoo.addons.queue_job.job import job
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from .common import PULL_REQUEST_STATES, MERGED


class GithubEvent(models.Model):

    _name = "github.event"
    _description = "Github Event"
    _rec_name = "pull_request_id"

    payload = fields.Text()
    payload_serialized = Serialized(
        compute='_compute_payload_serialized'
    )

    @api.depends('payload')
    def _compute_payload_serialized(self):
        events_with_payloads = self.filtered(lambda e: e.payload)
        for event in events_with_payloads:
            event.payload_serialized = json.loads(event.payload)

    action = fields.Char()
    state = fields.Selection(
        PULL_REQUEST_STATES,
    )
    date_payload = fields.Datetime()
    pull_request_id = fields.Many2one(
        'github.pull_request',
        'Pull Request',
        ondelete='restrict',
        index=True,
        copy=False,
    )
    title = fields.Char()

    def _get_value_from_payload(self, path):
        """Get a value from the payload.

        :param path: a doted notation of the path to access the value.
        :return: the value contained at the given path.
        """
        section = self.payload_serialized
        keys = path.split('.')

        for key in keys[:-1]:
            if not isinstance(section, dict) or key not in section:
                raise ValidationError(_(
                    "The payload does not contain a value at the path {}."
                ).format(path))

            section = section[key]

        return section[keys[-1]]

    def _find_existing_pull_request(self, url):
        return self.env['github.pull_request'].search([
            ('source', '=', url),
        ])

    def _make_pull_request(self, url):
        return self.env['github.pull_request'].create({'source': url})

    def _get_pull_request(self):
        url = self._get_value_from_payload('pull_request.html_url')
        existing_pull_request = self._find_existing_pull_request(url)
        return existing_pull_request or self._make_pull_request(url)

    def _get_action(self):
        return self._get_value_from_payload('action')

    def _get_state(self):
        is_merged = self._get_value_from_payload('pull_request.merged_at')
        return MERGED if is_merged else self._get_value_from_payload('pull_request.state')

    def _get_date_payload(self):
        datetime_string = self._get_value_from_payload('pull_request.updated_at')
        datetime_obj = dateutil.parser.parse(datetime_string)
        naive_datetime_string = datetime_obj.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return naive_datetime_string

    def _get_title(self):
        return self._get_value_from_payload("pull_request.title")

    def update_from_payload(self):
        """Update the event's data from its payload."""
        self.write({
            'action': self._get_action(),
            'pull_request_id': self._get_pull_request().id,
            'state': self._get_state(),
            'date_payload': self._get_date_payload(),
            'title': self._get_title(),
        })

    @job
    def process(self):
        """Process a single event."""
        self.update_from_payload()

        if self.pull_request_id.is_latest_event(self):
            self.pull_request_id.update_from_event(self)
