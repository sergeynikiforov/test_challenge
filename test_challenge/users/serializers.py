from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer
from allauth.account.forms import ResetPasswordForm
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from test_challenge.users.models import User, Team


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    DRF serializer for User model
    """
    team = serializers.HyperlinkedIdentityField(view_name="test_challenge:team-detail")

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'team')


class UserJWTSerializer(serializers.ModelSerializer):
    """
    DRF serializer for rest_auth USER_DETAILS_SERIALIZER
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    """
    DRF serializer for Team model
    """
    members = serializers.HyperlinkedRelatedField(many=True,
                                                  view_name='test_challenge:user-detail',
                                                  read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'members')


class TeamNestedSerializer(serializers.HyperlinkedModelSerializer):
    """
    DRF serializer to use with nested routing
    """
    members = NestedHyperlinkedRelatedField(many=True, read_only=True, view_name='test_challenge:user-detail',
                                            parent_lookup_kwargs={'team_pk': 'team_pk'})

    class Meta:
        model = Team
        fields = ('id', 'name', 'members')


class PasswordSerializer(PasswordResetSerializer):
    """
    Uses allauth's password reset form
    """
    password_reset_form_class = ResetPasswordForm
