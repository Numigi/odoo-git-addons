# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import re
from odoo import fields, models, api

regex_github_source = re.compile(
    r'https:\/\/(?P<host>[\w\.]+)/'
    r'(?P<organization>\w+)/'
    r'(?P<repository>[\w\-_]+)/'
    r'pull/'
    r'(?P<pull_request_number>\d+)'
)


class GithubPullRequest(models.Model):
    _name = "github.pull_request"
    _description = "Github Pull Request"

    source = fields.Char(required=True)
    state = fields.Selection(
        [('open', 'Open'), ('merged', 'Merged'), ('closed', 'Closed')],
        default='open',
    )
    developer_id = fields.Many2one('res.partner', 'Developer', ondelete='restrict', index=True)
    host = fields.Char(readonly=True)
    organization = fields.Char(readonly=True)
    repository = fields.Char(readonly=True)
    pull_request_number = fields.Integer(readony=True)

    _sql_constraints = [
        ('source', 'UNIQUE (source)', 'A Pull Request already exists for this source'),
    ]

    @api.model
    def create(self, vals):
        updated_vals = update_according_to_source(vals['source'], vals)
        return super().create(updated_vals)

    @api.multi
    def write(self, vals):
        updated_vals = update_according_to_source(vals.get('source', ''), vals)
        super().write(updated_vals)


def update_according_to_source(source: str, vals: dict) -> dict :
    res = re.match(regex_github_source, source)
    if res:
        vals.update(res.groupdict())
    return vals
