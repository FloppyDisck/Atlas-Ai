import unittest
from custom_actions.action_reminder_set import CurrentReminders

class TestReminderSet(unittest.TestCase):
    def setUp(self):
        self.reminder = CurrentReminders()
    def test_clear_list(self):
        self.reminder.clear_list()