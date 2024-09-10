# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

import pytz
from odoo import models, fields, api

organisation_default_series = (
    '12.0',
    '13.0',
    '14.0',
    '15.0',
    '16.0',
    '17.0',
)


class OdooModuleChatter(models.Model):
    _name = "odoo.module"
    _inherit = ['odoo.module', 'mail.thread', 'mail.activity.mixin']


class GithubRepoBranch(models.Model):
    _inherit = 'github.repository.branch'

    # add the ./addons/ folder so it is also scanned in client repo
    # TA#16291
    module_paths = fields.Text(default="./\n./addons")


class GithubOrganization(models.Model):
    _inherit = 'github.organization'

    @api.model
    def create_from_name(self, name):
        ret = super().create_from_name(name)
        series_obj = self.env['github.organization.serie']
        details = [
            {'sequence': i, 'name': name, 'organization_id': ret.id}
            for i, name in enumerate(organisation_default_series)
        ]
        series_obj.create(details)


class AbstractGithubModel(models.AbstractModel):
    _inherit = "abstract.github.model"

    def process_timezone_fields(self, res):
        """ 
        This method replaces the original method from the abstract model 
        from OCA Module github_connector.
        """
        for k, v in res.items():
            if self._fields[k].type == "datetime":
                if isinstance(v, str):
                    res[k] = datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
                elif isinstance(v, datetime) and v.tzinfo:
                    res[k] = v.astimezone(pytz.utc).replace(tzinfo=None)
