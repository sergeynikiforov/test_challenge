from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'test_challenge.users'
    verbose_name = "Users"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        import  test_challenge.users.signals #noqa
