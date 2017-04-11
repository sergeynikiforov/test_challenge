from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings


from test_challenge.users.models import Team, User
from test_challenge.users.serializers import TeamSerializer, UserSerializer, TeamNestedSerializer
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


class TeamNestedViewSet(viewsets.GenericViewSet):
    """
    Team ViewSet nested within Users
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, member_pk=None, format=None):
        queryset = self.get_queryset().filter(member__pk=member_pk)
        serializer = TeamSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, member_pk=None, format=None):
        queryset = self.get_queryset().filter(member__pk=member_pk)
        team = get_object_or_404(queryset, pk=pk)
        serializer = TeamSerializer(team, context={'request': request})
        return Response(serializer.data)

    def update(self, request, *args, pk=None, member_pk=None, format=None, **kwargs):
        partial = kwargs.pop('partial', False)
        # check if User is part of that particular Team
        queryset = self.get_queryset().filter(member__pk=member_pk)
        instance = get_object_or_404(queryset, pk=pk)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def create(self, request, *args, member_pk=None, **kwargs):
        # make sure the user doesn't have a team already
        user = get_object_or_404(User.objects.all(), pk=member_pk)
        if user.team:
            return Response({'error': 'User already has a Team'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = self.perform_create(serializer)
        user.team = team
        user.save()

        # update team instance
        serializer_upd = self.get_serializer(team)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer_upd.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedAndIsAdminIfUpdated,)
