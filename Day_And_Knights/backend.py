
from social_core.backends.auth0 import Auth0OAuth2

class CustomAuth0Backend(Auth0OAuth2):
    def user_data(self, access_token, *args, **kwargs):
        data = super().user_data(access_token, *args, **kwargs)
        return {
            'username': data.get('sub'),
            'email': data.get('email'),
            'first_name': data.get('given_name', ''),
            'last_name': data.get('family_name', ''),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }