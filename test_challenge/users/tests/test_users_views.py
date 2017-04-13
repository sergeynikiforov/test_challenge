import pytest

from test_plus.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework_jwt.settings import api_settings
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from test_challenge.users.models import User, Team


@pytest.mark.users
class TestViews(TestCase):
    TEST_EMAIL = 'test@test.com'
    TEST_PASSWORD = 'password123'
    TEST_TEAM_NAME = 'test_team'

    def setUp(self):
        self.jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        self.jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        self.test_team = Team(name=self.TEST_TEAM_NAME)
        self.test_team.save()
        self.test_user = User(email=self.TEST_EMAIL, password=self.TEST_PASSWORD, team=self.test_team)
        self.test_user.save()

        payload = self.jwt_payload_handler(self.test_user)
        self.token = self.jwt_encode_handler(payload)
        self.client = APIClient()

    def test_team_get_list_authorized(self):
        """Test Teams list response code authorized"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.get(reverse('test_challenge:team-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_get_list_unauthorized(self):
        """Test Teams list response code unauthorized"""
        self.client.credentials()
        response = self.client.get(reverse('test_challenge:team-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_team_get_detail_authorized(self):
        """Test Teams detail response code authorized"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.get(reverse('test_challenge:team-detail', kwargs={'pk': '{}'.format(self.test_team.pk)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_get_detail_unauthorized(self):
        """Test Teams detail response code unauthorized"""
        self.client.credentials()
        response = self.client.get(reverse('test_challenge:team-detail', kwargs={'pk': '{}'.format(self.test_team.pk)}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_team_get_list_return_type(self):
        """Test team get list returns list-like type"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.get(reverse('test_challenge:team-list'))
        self.assertEqual(type(response.data['results']), ReturnList)

    def test_team_get_detail_return_type(self):
        """Test team get list returns dict-like type"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.get(reverse('test_challenge:team-detail', kwargs={'pk': '{}'.format(self.test_team.pk)}))
        self.assertEqual(type(response.data), ReturnDict)

    def test_team_post_not_allowed(self):
        """Tests Teams POST not allowed"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.post(reverse('test_challenge:team-list'), {'name': 'new_team'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_team_delete_not_allowed(self):
        """Tests Teams DELETE not allowed"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.delete(reverse('test_challenge:team-detail',
                                              kwargs={'pk': '{}'.format(self.test_team.pk)}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_team_put_authorized_by_member(self):
        """Tests Teams PUT by authorized member returns 200"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.put(reverse('test_challenge:team-detail', kwargs={'pk': '{}'.format(self.test_team.pk)}),
                                   {'name': 'new_name'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_patch_authorized_by_member(self):
        """Tests Teams PATCH by authorized member returns 200"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.patch(reverse('test_challenge:team-detail',
                                             kwargs={'pk': '{}'.format(self.test_team.pk)}),
                                   {'name': 'new_name'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_put_authorized_by_not_member(self):
        """Tests Teams PUT by authorized user but not a member returns 403"""
        other_user = User(email='other@test.com', password='new_pass2', first_name='Alice')
        other_user.save()
        payload = self.jwt_payload_handler(other_user)
        other_user_token = self.jwt_encode_handler(payload)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + other_user_token)
        response = self.client.put(reverse('test_challenge:team-detail', kwargs={'pk': '{}'.format(self.test_team.pk)}),
                                   {'name': 'new_name'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_team_patch_authorized_by_not_member(self):
        """Tests Teams PATCH by authorized user but not a member returns 403"""
        other_user = User(email='other@test.com', password='new_pass2', first_name='Alice')
        other_user.save()
        payload = self.jwt_payload_handler(other_user)
        other_user_token = self.jwt_encode_handler(payload)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + other_user_token)
        response = self.client.patch(reverse('test_challenge:team-detail',
                                             kwargs={'pk': '{}'.format(self.test_team.pk)}),
                                   {'name': 'new_name'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_list_authorized(self):
        """Test Users list response code authorized"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.get(reverse('test_challenge:user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_list_unauthorized(self):
        """Test Users list response code unauthorized"""
        self.client.credentials()
        response = self.client.get(reverse('test_challenge:user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_get_detail_authorized(self):
        """Test Users detail response code for authorized user"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.get(reverse('test_challenge:user-detail', kwargs={'pk': '{}'.format(self.test_user.pk)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_detail_unauthorized(self):
        """Test Users detail response code for unauthorized user"""
        self.client.credentials()
        response = self.client.get(reverse('test_challenge:user-detail', kwargs={'pk': '{}'.format(self.test_user.pk)}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_get_list_return_type(self):
        """Test Users get list returns list-like type"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.get(reverse('test_challenge:user-list'))
        self.assertEqual(type(response.data['results']), ReturnList)

    def test_user_get_detail_return_type(self):
        """Test Users get list returns dict-like type"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.get(reverse('test_challenge:user-detail', kwargs={'pk': '{}'.format(self.test_user.pk)}))
        self.assertEqual(type(response.data), ReturnDict)

    def test_user_post_not_allowed(self):
        """Tests Users POST not allowed"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.post(reverse('test_challenge:user-list'),
                                    {'email': 'email@example.com',
                                     'password': 'test_password1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_delete_not_allowed(self):
        """Tests Users DELETE not allowed"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.delete(reverse('test_challenge:team-detail',
                                              kwargs={'pk': '{}'.format(self.test_user.pk)}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_can_patch_self(self):
        """Test User can PATCH self"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.patch(reverse('test_challenge:user-detail',
                                             kwargs={'pk': '{}'.format(self.test_user.pk)}),
                                     {'first_name': 'new_first_name'},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_first_name = User.objects.get(email=self.TEST_EMAIL).first_name
        self.assertEqual(new_first_name, 'new_first_name')

    def test_user_cannot_patch_other(self):
        """Test User cannot patch other users"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        other_user = User(email='other@test.com', password='new_pass2', first_name='Alice')
        other_user.save()

        response = self.client.patch(reverse('test_challenge:user-detail',
                                             kwargs={'pk': '{}'.format(other_user.pk)}),
                                     {'first_name': 'Bob'},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        alice = User.objects.get(email='other@test.com')
        self.assertEqual(alice.first_name, 'Alice')

    def test_user_admin_can_patch_others(self):
        """Tests admin user can PATCH other users"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        self.test_user.is_admin = True
        self.test_user.save()

        other_user = User(email='other@test.com', password='new_pass2', first_name='Alice')
        other_user.save()

        response = self.client.patch(reverse('test_challenge:user-detail',
                                             kwargs={'pk': '{}'.format(other_user.pk)}),
                                     {'first_name': 'Bob'},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        former_alice = User.objects.get(email='other@test.com')
        self.assertEqual(former_alice.first_name, 'Bob')

    def test_user_invite(self):
        """Tests user invite functionality (can invite, email is present)"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.post(reverse('test_challenge:user-invite',
                                            kwargs={'pk': '{}'.format(self.test_user.pk)}),
                                    {'email': 'email@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        no_email_response = self.client.post(reverse('test_challenge:user-invite',
                                                     kwargs={'pk': '{}'.format(self.test_user.pk)}),
                                             {}, format='json')
        self.assertEqual(no_email_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nested_team_get_list(self):
        """Tests GET on nested User's Team - verifies that it shows team of this user"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        other_team = Team(name='other_team')
        other_team.save()
        other_user = User(email='other@test.com', password='new_pass2', first_name='Alice')
        other_user.team = other_team
        other_user.save()

        response = self.client.get(reverse('test_challenge:users-team-list',
                                           kwargs={'member_pk': '{}'.format(self.test_user.pk)}))

        # check status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check it's a list-like of len 1 (we have foreign key... so far)
        self.assertEqual(type(response.data), ReturnList)
        self.assertEqual(len(response.data), 1)

        # test it is what it is =)
        self.assertEqual(response.data[0]['id'], self.test_team.pk)

    def test_nested_team_get_detail(self):
        """Tests GET on nested User's Team detail view"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        other_team = Team(name='other_team')
        other_team.save()
        other_user = User(email='other@test.com', password='new_pass2', first_name='Alice')
        other_user.team = other_team
        other_user.save()

        response = self.client.get(reverse('test_challenge:users-team-detail',
                                           kwargs={'member_pk': '{}'.format(self.test_user.pk),
                                                   'pk': '{}'.format(self.test_team.pk)}))

        # check status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check it's a dict-like
        self.assertEqual(type(response.data), ReturnDict)
        self.assertEqual(response.data['id'], self.test_team.pk)

    def test_nested_team_can_be_updated_only_by_members(self):
        """Tests PUT, PATCH on nested User's Team - it can be updated only by its members"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        other_team = Team(name='other_team')
        other_team.save()
        other_user = User(email='other@test.com', password='new_pass2', first_name='Alice')
        other_user.team = other_team
        other_user.save()

        # try to patch other_team when you're a member of test_team
        response = self.client.patch(reverse('test_challenge:users-team-detail',
                                             kwargs={'member_pk': '{}'.format(other_user.pk),
                                                     'pk': '{}'.format(other_team.pk)}),
                                     {'name': 'new_name_for_other_team'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try to patch your team
        response = self.client.patch(reverse('test_challenge:users-team-detail',
                                             kwargs={'member_pk': '{}'.format(self.test_user.pk),
                                                     'pk': '{}'.format(self.test_team.pk)}),
                                     {'name': 'new_name_for_test_team'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_nested_team_post(self):
        """Tests User can POST to nested Team url when he/she doesn't have one yet"""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        # test for 400
        response = self.client.post(reverse('test_challenge:users-team-list',
                                            kwargs={'member_pk': '{}'.format(self.test_user.pk)}),
                                    {'name': 'new_test_team'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # unlink test_team from the user, try POST once again
        self.test_user.team = None
        self.test_user.save()
        response = self.client.post(reverse('test_challenge:users-team-list',
                                            kwargs={'member_pk': '{}'.format(self.test_user.pk)}),
                                    {'name': 'new_test_team'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=self.TEST_EMAIL)
        self.assertEqual(user.team.name, 'new_test_team')

    def test_api_root(self):
        """Tests api root access"""
        response = self.client.get(reverse('test_challenge:api-root'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = self.client.get(reverse('test_challenge:api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
