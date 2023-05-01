from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from Day_And_Knights.models import Player

class PlayerBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            player = Player.objects.get(username=username)
            if player.check_password(password):
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    # Create a new user object for the player
                    user = User(username=username, password=player.password)
                    user.save()
                return user
        except Player.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None