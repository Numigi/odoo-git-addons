# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models, api


class GithubPullRequestTask(models.Model):
    _inherit = "github.pull_request"
    task_ids = fields.Many2many(
        'project.task',
        'pull_request_task_ref',
        'pull_request_id',
        'task_id',
        string='Tasks'
    )


def evaluate_pull_request_states(task):
    return not task.pull_request_ids.filtered(lambda pr: pr.state == "open")


class ProjectTaskPullRequest(models.Model):
    _inherit = "project.task"
    pull_request_ids = fields.Many2many(
        'github.pull_request',
        'pull_request_task_ref',
        'task_id',
        'pull_request_id',
        string='Pull Requests'
    )

    def _compute_pull_request_qty(self):
        for record in self:
            record.pull_request_qty = len(record.pull_request_ids)

    pull_request_qty = fields.Integer(compute="_compute_pull_request_qty")

    def _check_all_pull_request_state(self):
        for record in self:
            record.overall_pull_request_state = evaluate_pull_request_states(record)

    overall_pull_request_state = fields.Boolean(
        readonly=True, compute="_check_all_pull_request_state"
    )

    @api.onchange("pull_request_ids")
    def _all_pull_request_ready_on_change(self):
        for record in self:
            record.all_pull_request_ready = evaluate_pull_request_states(record)
