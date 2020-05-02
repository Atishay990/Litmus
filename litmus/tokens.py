""" When a new user registers, a unique token is generated eveytime which in turn generates new link for homepage,
    which is then sent as a mail to registered user e-mail. """

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (
        text_type(user.pk) + text_type(timestamp) +
        text_type(user.profile.signup_confirmation)
        )

account_activation_token = AccountActivationTokenGenerator()
