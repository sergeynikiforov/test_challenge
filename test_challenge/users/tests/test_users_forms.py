import pytest

from django.contrib.auth import get_user_model
from test_plus.test import TestCase

from test_challenge.users.forms import UserCreationForm, UserChangeForm
from test_challenge.users.tests.factories import UserFactory


@pytest.mark.users
class TestUserCreationForm(TestCase):
    def setUp(self):
        self.test_email = 'test@test.com'
        self.test_password_1 = 'password123'
        self.test_password_2 = 'password456'

    @pytest.mark.django_db
    def test_form_is_invalid_when_passwords_dont_match(self):
        self.assertFalse(
            UserCreationForm({
                'email': self.test_email,
                'password1': self.test_password_1,
                'password2': self.test_password_2,
            }).is_valid()
        )

    @pytest.mark.django_db
    def test_form_is_valid_when_passwords_match(self):
        self.assertTrue(
            UserCreationForm({
                'email': self.test_email,
                'password1': self.test_password_1,
                'password2': self.test_password_1,
            }).is_valid()
        )

    @pytest.mark.django_db
    def test_save_password_hashed(self):
        """Checks if the form's save function saves password in a hashed format"""
        user = UserCreationForm({
                'email': self.test_email,
                'password1': self.test_password_1,
                'password2': self.test_password_1,
            }).save()
        self.assertFalse(user.password == self.test_password_1)

    @pytest.mark.django_db
    def test_save_doesnt_save_on_commit_false(self):
        UserCreationForm({
            'email': self.test_email,
            'password1': self.test_password_1,
            'password2': self.test_password_1,
        }).save(commit=False)
        self.assertEqual(get_user_model().objects.all().count(), 0)

    @pytest.mark.django_db
    def test_save_actually_saves_on_commit_true(self):
        UserCreationForm({
            'email': self.test_email,
            'password1': self.test_password_1,
            'password2': self.test_password_1,
        }).save(commit=True)
        self.assertEqual(get_user_model().objects.all().count(), 1)


@pytest.mark.users
class TestUserChangeForm(TestCase):
    def setUp(self):
        self.test_email = 'test@test.com'
        self.test_password = 'password'

    @pytest.mark.django_db
    def test_form_doesnt_change_password(self):
        user = UserFactory(email=self.test_email)
        initial_password = user.password
        changed_user = UserChangeForm({
            'email': self.test_email,
            'password': 'new_pass',
        }, instance=user).save()
        self.assertEqual(initial_password, changed_user.password)
