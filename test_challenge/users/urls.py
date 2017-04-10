from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested import routers

from test_challenge.users.views import api_root, UserViewSet, TeamViewSet, TeamNestedViewSet


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)

users_router = routers.NestedSimpleRouter(router, r'users', lookup='member')
users_router.register(r'teams', TeamNestedViewSet)

urlpatterns = format_suffix_patterns([url(r'^$', api_root)] + router.urls + users_router.urls)

# urlpatterns = format_suffix_patterns([
#     url(r'^$', api_root),
#     url(r'^users/$', UserList.as_view(), name='user-list'),
#     url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),
#     url(r'^teams/$', TeamList.as_view(), name='team-list'),
#     url(r'^teams/(?P<pk>[0-9]+)/$', TeamDetail.as_view(), name='team-detail'),
# ])
