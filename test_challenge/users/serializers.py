from rest_framework import serializers

from test_challenge.users.models import User, Team


class UserSerializer(serializers.ModelSerializer):
    """
    DRF serializer for User model
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'team')


class TeamSerializer(serializers.ModelSerializer):
    """
    DRF serializer for Team model
    """
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Team
        fields = ('id', 'name', 'members')
