from rest_framework_nested import routers

from test_challenge.users.views import UserViewSet, TeamViewSet, TeamNestedViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)

users_router = routers.NestedSimpleRouter(router, r'users', lookup='member')
users_router.register(r'teams', TeamNestedViewSet, base_name='users-team')

urlpatterns = router.urls + users_router.urls
