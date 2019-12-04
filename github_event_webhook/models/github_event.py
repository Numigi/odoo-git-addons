# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.addons.queue_job.job import job


class GithubEvent(models.Model):

    _inherit = "github.event"

    @job
    def process_job(self):
        """Process a github event."""
        self.process()
