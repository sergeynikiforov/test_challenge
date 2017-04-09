import factory


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_admin = False
    team = factory.SubFactory('test_challenge.users.tests.factories.TeamFactory')
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = 'users.User'
        django_get_or_create = ('email', )


class TeamFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('color_name')

    class Meta:
        model = 'users.Team'
