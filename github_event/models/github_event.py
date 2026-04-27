# Copyright 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class GithubEvent(models.Model):
    _name = "github.event"
    _description = "Github Event"
    _order = "id desc"

    action = fields.Char()
    payload = fields.Text()

    # Odoo 18: Utilisation du champ Json natif à la place de Serialized
    payload_serialized = fields.Json(compute="_compute_payload_serialized")

    @api.depends("payload")
    def _compute_payload_serialized(self):
        for event in self:
            if event.payload:
                try:
                    event.payload_serialized = json.loads(event.payload)
                except json.JSONDecodeError:
                    event.payload_serialized = {}
            else:
                event.payload_serialized = {}

    def _get_value_from_payload(self, path):
        """Get a value from the payload.

        :param path: a doted notation of the path to access the value.
        :return: the value contained at the given path.
        """
        section = self.payload_serialized or {}
        keys = path.split(".")

        for key in keys[:-1]:
            if not isinstance(section, dict) or key not in section:
                raise ValidationError(
                    _("The payload does not contain a value at the path {}.").format(
                        path
                    )
                )

            section = section[key]

        if not isinstance(section, dict) or keys[-1] not in section:
            raise ValidationError(
                _("The payload does not contain a value at the path {}.").format(path)
            )

        return section[keys[-1]]

    def process(self):
        """Process a github event.

        This method is intended to be inherited by other modules
        to add extra behavior when processing a github event.
        """
        self.action = self._get_value_from_payload("action")
