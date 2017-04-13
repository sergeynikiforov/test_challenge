import pytest

from test_plus.test import TestCase
from invitations.models import Invitation
from invitations.signals import invite_accepted

from test_challenge.users.models import User, Team


@pytest.mark.users
class TestUsersSignals(TestCase):
    TEST_EMAIL = 'test@test.com'
    TEST_PASSWORD = 'password123'
    TEST_TEAM_NAME = 'test_team'

    def setUp(self):
        self.test_team = Team(name=self.TEST_TEAM_NAME)
        self.test_team.save()
        self.test_user = User(email=self.TEST_EMAIL, password=self.TEST_PASSWORD, team=self.test_team)
        self.test_user.save()

    def test_invite_accepted_receiver(self):
        """Artificially sends invite_accepted signal, tests if the invitee gets the inviter's team"""
        invitee_email = 'invitee@example.com'
        invitee = User(email=invitee_email, password='invitee_pwd1', first_name='Alice')
        invitee.save()
        invitation = Invitation.create(invitee_email, inviter=self.test_user)
        invite_accepted.send(sender=Invitation, email=invitation.email)
        invitee.refresh_from_db()
        self.assertEqual(invitee.team, self.test_user.team)
