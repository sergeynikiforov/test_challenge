import pytest
from test_plus.test import TestCase

from test_challenge.users.tests.factories import UserFactory, TeamFactory
from test_challenge.users.models import User


@pytest.mark.users
class TestUserManager(TestCase):
    def setUp(self):
        self.test_email = 'test@test.com'
        self.test_password = 'password123'

    def test_create_user_raises_value_error_(self):
        with self.assertRaises(ValueError):
            User.objects.create_user('', self.test_password)

    @pytest.mark.django_db
    def test_create_user_creates_and_saves_user(self):
        User.objects.create_user(self.test_email, self.test_password)
        self.assertEqual(self.test_email, User.objects.get(email=self.test_email).email)

    @pytest.mark.django_db
    def test_create_superuser_creates_superuser(self):
        User.objects.create_superuser(self.test_email, self.test_password)
        self.assertTrue(User.objects.get(email=self.test_email).is_admin)
        self.assertTrue(User.objects.get(email=self.test_email).is_superuser)


@pytest.mark.users
class TestUsers(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test__str__(self):
        self.assertEqual(self.user.__str__(), self.user.email)

    def test_get_full_name_returns_email(self):
        usr = UserFactory(first_name='', last_name='')
        self.assertEqual(usr.get_full_name(), usr.email)

    def test_get_full_name_returns_first_last_name(self):
        first_name_user = UserFactory(first_name='John', last_name='')
        self.assertEqual(first_name_user.get_full_name(), first_name_user.first_name)

        last_name_user = UserFactory(first_name='', last_name='Smith')
        self.assertEqual(last_name_user.get_full_name(), last_name_user.last_name)

        # check full name as well
        self.assertEqual(self.user.get_full_name(), self.user.first_name + ' ' + self.user.last_name)

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), self.user.email)

    def test_is_staff_returns_is_admin(self):
        admin = UserFactory(is_admin=True)
        regular = UserFactory(is_admin=False)
        self.assertTrue(admin.is_staff)
        self.assertFalse(regular.is_staff)


@pytest.mark.users
class TestTeams(TestCase):
    def setUp(self):
        self.team = TeamFactory()

    def test__str__(self):
        self.assertEqual(self.team.__str__(), self.team.name)
