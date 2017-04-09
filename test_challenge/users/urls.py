from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from test_challenge.users.views import TeamDetail, TeamList, UserDetail, UserList

urlpatterns = format_suffix_patterns([
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^teams/$', TeamList.as_view()),
    url(r'^teams/(?P<pk>[0-9]+)/$', TeamDetail.as_view()),
])
