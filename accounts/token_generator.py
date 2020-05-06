from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()

# we import six from django utils. Six provides simple utilities for wrapping over differences between Python 2 and Python 3.
#we create a method _make_hash_value which overrides PasswordTokenGenerator method.
# we return user id, timestamp and user is active using the six imported from django utils.
# we return user id, timestamp and user is active using the six imported from django utils.
