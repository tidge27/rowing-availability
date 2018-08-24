import django
import logging
from django.contrib.auth.backends import RemoteUserBackend
from ucamwebauth import RavenResponse
from ucamwebauth.exceptions import UserNotAuthorised, OtherStatusCode
from ucamwebauth.utils import setting
from .models import MyUser

# Majority of this function copied from ucamwebauth, with some small changes to get email addresses etc.

logger = logging.getLogger(__name__)

# We inherit the automatic-user-creation code from RemoteUserBackend.
class CustomRavenAuthBackend(RemoteUserBackend):
    """An authentication backend for django that uses Raven.  To use, add
    'ucamwebauth.backends.RavenAuthBackend' to AUTHENTICATION_BACKENDS
    in your django settings.py."""

    def authenticate(self, request=None, remote_user=None):
        """Checks a response from the Raven server and sees if it is valid.  If
        it is, returns the User with the same username as the Raven username.
        @return User object, or None if authentication failed"""

        # Check that everything is correct, and return
        try:
            response = RavenResponse(request)
        except Exception as e:
            logger.error("%s: %s" % (type(e).__name__, e))
            raise

        if not response.validate():
            raise OtherStatusCode("The WLS returned status %d: %s" %
                                  (response.status, response.STATUS[response.status]))

        if (response.ver == 3) and (setting('UCAMWEBAUTH_NOT_CURRENT', default=False) is False) and \
                ('current' not in response.ptags):
            logger.error("%s: %s" % ("UserNotAuthorised", "Authentication successful but you are not authorised to "
                                                          "access this site"))
            raise UserNotAuthorised("Authentication successful but you are not authorised to access this site")

        if django.VERSION[0] <= 1 and django.VERSION[1] <= 10:
            user = super(CustomRavenAuthBackend, self).authenticate("".join([response.principal, "@cam.ac.uk"]))
        else:
            user = super(CustomRavenAuthBackend, self).authenticate(request, "".join([response.principal, "@cam.ac.uk"]))

        # creates (if necessary) the UserProfile model and update the raven_for_life property from the RavenResponse
        if user:
            profile = MyUser.objects.get_or_create(email=user)[0]
            profile.crsid = str(response.principal)
            profile.save()

        return user

    # Backwards compatibility: honour UCAMWEBAUTH_CREATE_USER.
    # @property
    # def create_unknown_user(self):
    #     return setting('UCAMWEBAUTH_CREATE_USER', default=True)
