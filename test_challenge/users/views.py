from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from test_challenge.users.models import Team, User
from test_challenge.users.serializers import TeamSerializer, UserSerializer


class TeamList(ListCreateAPIView):
    """
    List view for Teams, with create()
    """
    permission_classes = (IsAuthenticated,)

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetail(RetrieveUpdateDestroyAPIView):
    """
    Detail view for a Team
    """
    permission_classes = (IsAuthenticated,)

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class UserList(ListAPIView):
    """
    List view for Users
    """
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):
    """
    Detail view for a User
    """
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer
