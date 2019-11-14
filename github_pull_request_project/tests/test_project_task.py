# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests import common


class TestProjectTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pull_request_open = cls.env["github.pull_request"].create({
            "source": "https://github.com/Numigi/odoo-git-addons/pull/1",
            "state": "open"
        })
        cls.pull_request_closed = cls.env["github.pull_request"].create({
            "source": "https://github.com/Numigi/odoo-git-addons/pull/2",
            "state": "closed"
        })
        cls.pull_request_merged = cls.env["github.pull_request"].create({
            "source": "https://github.com/Numigi/odoo-git-addons/pull/3",
            "state": "merged"
        })

    # Simple cases
    def test_whenNoPR_thenTaskReady(self):
        task = self.env["project.task"].create({
            "name": "ttask", "pull_request_ids": [(5, False, False)]
        })
        assert task.no_pull_request_open

    def test_whenPrAreMerged_thenTaskReady(self):
        task = self.env["project.task"].create({
            "name": "ttask", "pull_request_ids": [(6, False, (self.pull_request_merged.id,))]
        })
        assert task.no_pull_request_open

    def test_whenPrAreClosed_thenTaskReady(self):
        task = self.env["project.task"].create({
            "name": "ttask", "pull_request_ids": [(6, False, (self.pull_request_closed.id,))]
        })
        assert task.no_pull_request_open

    def test_whenPrAreOpen_thenTaskNotReady(self):
        task = self.env["project.task"].create({
            "name": "ttask", "pull_request_ids": [(6, False, (self.pull_request_open.id,))]
        })
        assert not task.no_pull_request_open

    # Mixing cases
    def test_whenAllStates_thenTaskNotReady(self):
        task = self.env["project.task"].create({
            "name": "ttask",
            "pull_request_ids": [(
                6, False,
                (
                    self.pull_request_open.id,
                    self.pull_request_closed.id,
                    self.pull_request_merged.id
                )
            )]
        })
        assert not task.no_pull_request_open

    def test_whenClosedAndMerged_thenTaskReady(self):
        task = self.env["project.task"].create({
            "name": "ttask",
            "pull_request_ids": [(
                6, False, (self.pull_request_closed.id, self.pull_request_merged.id)
            )]
        })
        assert task.no_pull_request_open

    def test_whenMergedAndOpen_thenTaskNotReady(self):
        task = self.env["project.task"].create({
            "name": "ttask",
            "pull_request_ids": [(
                6, False, (self.pull_request_merged.id, self.pull_request_open.id)
            )]
        })
        assert not task.no_pull_request_open

    def test_whenClosedAndOpen_thenTaskNotReady(self):
        task = self.env["project.task"].create({
            "name": "ttask",
            "pull_request_ids": [(
                6, False, (self.pull_request_closed.id, self.pull_request_open.id)
            )]
        })
        assert not task.no_pull_request_open
