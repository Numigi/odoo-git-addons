# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests import common
from ddt import ddt, data, unpack


@ddt
class TestPullRequest(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.github_pull_request_pool = cls.env["github.pull_request"]

    @data(
        {
            'url': "https://github.com/Numigi/odoo_git_addons/pull/108693",
            'expected': {
                'organization': 'Numigi',
                'host': 'github.com',
                'repository': 'odoo_git_addons',
                'pull_request_number':108693,
            }
        },
        {
            'url': "https://github.com/Numigi/odoo-git-addons/pull/1",
            'expected': {
                'organization': 'Numigi',
                'host': 'github.com',
                'repository': 'odoo-git-addons',
                'pull_request_number': 1,
            }
        },
    )
    @unpack
    def test_whenPrIsCreatedFromURL_thenFieldsAreFilled(self, url, expected):
        pr = self.github_pull_request_pool.create({'source': url})
        assert pr.organization == expected['organization']
        assert pr.host == expected['host']
        assert pr.repository == expected['repository']
        assert pr.pull_request_number == expected['pull_request_number']

    @data(
        {
            'url': "https://github.com/Numigi/odoo_git_addons/pull/108693",
            'expected': {
                'organization': 'Numigi',
                'host': 'github.com',
                'repository': 'odoo_git_addons',
                'pull_request_number':108693,
            }
        },
        {
            'url': "https://github.com/Numigi/odoo-git-addons/pull/1",
            'expected': {
                'organization': 'Numigi',
                'host': 'github.com',
                'repository': 'odoo-git-addons',
                'pull_request_number': 1,
            }
        },
    )
    @unpack
    def test_whenPrIsUpdatedFromURL_thenFieldsAreUpdated(self, url, expected):
        pr = self.github_pull_request_pool.create({'source': "https://github.com/Numigi/odoo-public/pull/666"})
        pr.source = url
        assert pr.organization == expected['organization']
        assert pr.host == expected['host']
        assert pr.repository == expected['repository']
        assert pr.pull_request_number == expected['pull_request_number']
