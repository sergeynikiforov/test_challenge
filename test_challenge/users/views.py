from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins


from test_challenge.users.models import Team, User
from test_challenge.users.serializers import TeamSerializer, UserSerializer
from test_challenge.users.permissions import IsAuthenticatedAndIsAdminIfUpdated


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'teams': reverse('team-list', request=request, format=format)
    })


class TeamViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated,)

    # def list(self, request, format=None):
    #     queryset = Team.objects.all()
    #     serializer = TeamSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None, format=None):
    #     queryset = Team.objects.all()
    #     team = get_object_or_404(queryset, pk=pk)
    #     serializer = TeamSerializer(team, context={'request': request})
    #     return Response(serializer.data)


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedAndIsAdminIfUpdated,)

    # def list(self, request, format=None):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None, format=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user, context={'request': request})
    #     return Response(serializer.data)
    #
    # def update(self, request, pk=None, format=None):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
