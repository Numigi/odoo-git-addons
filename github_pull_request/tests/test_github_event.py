# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import os
from odoo.tests import common
from ddt import ddt, data, unpack


@ddt
class TestGithubEvent(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event_1 = cls.env['github.event'].create({})
        cls.event_2 = cls.env['github.event'].create({})

    def _read_payload(self, filename):
        test_folder = os.path.dirname(os.path.realpath(__file__))
        payload_file_path = os.path.join(test_folder, 'data', filename)
        with open(payload_file_path, 'r') as file:
            return file.read()

    def test_if_not_existing_pull_request__new_pull_request_created(self):
        self.event_1.payload = self._read_payload('pull_request_2_reopened.json')
        self.event_1.process()
        assert self.event_1.pull_request_id

    def test_action(self):
        self.event_1.payload = self._read_payload('pull_request_2_reopened.json')
        self.event_1.process()
        assert self.event_1.action == 'reopened'

    @data(
        ('pull_request_1_merged.json', 'merged'),
        ('pull_request_2_closed.json', 'closed'),
        ('pull_request_2_reopened.json', 'open'),
    )
    @unpack
    def test_status(self, filename, expected_state):
        self.event_1.payload = self._read_payload(filename)
        self.event_1.process()
        assert self.event_1.pull_request_id.state == expected_state

    @data(
        ('pull_request_2_closed.json', 'pull_request_2_reopened.json'),
        ('pull_request_2_reopened.json', 'pull_request_2_closed.json'),
    )
    @unpack
    def test_if_not_last_event__pull_request_not_updated(self, first_event, second_event):
        """Test that the pull request is only updated by the latest event.

        The event pull_request_closed is updated at: 2019-11-22T17:12:05Z
        The event pull_request_reopened  is updated at: 2019-11-22T17:50:29Z

        The final result is that the pull request is open, because
        the pull request is closed, then reopened.

        This result must not depend on whether one event is processed before the other.
        """
        self.event_1.payload = self._read_payload(first_event)
        self.event_2.payload = self._read_payload(second_event)
        self.event_1.process()
        self.event_2.process()
        assert self.event_1.pull_request_id == self.event_2.pull_request_id
        assert self.event_1.pull_request_id.state == 'open'
