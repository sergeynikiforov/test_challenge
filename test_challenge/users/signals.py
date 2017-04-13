from django.dispatch import receiver
from invitations.signals import invite_accepted
from invitations.models import Invitation

from test_challenge.users.models import User


@receiver(invite_accepted, sender=Invitation)
def assign_team(sender, email, **kwargs):
    """
    Assigns the invited user to the team of the inviter.
    The sender is Invitation, as invite_accepted fires only after the invitee signup
    """
    try:
        invitation = Invitation.objects.get(email=email)
        user = User.objects.get(email=email)
        user.team = invitation.inviter.team
        user.save()
    except Invitation.DoesNotExist:
        pass
    except User.DoesNotExist:
        pass
