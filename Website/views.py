import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.shortcuts import get_object_or_404, render
from django.views import View
from Day_And_Knights.models import Match, Player, Team
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from requests_oauthlib import OAuth2Session
import requests

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def login(request):
    auth0 = OAuth2Session(
        settings.AUTH0_CLIENT_ID,
        redirect_uri=request.build_absolute_uri(reverse('callback')),
        scope=settings.SOCIAL_AUTH_AUTH0_SCOPE,
    )
    authorization_url, _ = auth0.authorization_url(settings.AUTH0_AUTHORIZE_URL)

    return redirect(authorization_url)


def callback(request):
    code = request.GET.get('code')
    token_url = "https://{0}/oauth/token".format(settings.AUTH0_DOMAIN)
    token_payload = {
        "client_id": settings.AUTH0_CLIENT_ID,
        "client_secret": settings.AUTH0_CLIENT_SECRET,
        "redirect_uri": request.build_absolute_uri(reverse("callback")),
        "code": code,
        "grant_type": "authorization_code",
    }
    token_headers = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.post(token_url, data=token_payload, headers=token_headers)
    if response.ok:
        token_info = response.json()
        id_token = token_info['id_token']
        user_info_url = "https://{0}/userinfo".format(settings.AUTH0_DOMAIN)
        user_info_headers = {"Authorization": "Bearer {0}".format(id_token)}

        user_info_response = requests.get(user_info_url, headers=user_info_headers)
        if user_info_response.ok:
            user_info = user_info_response.json()
            sub = user_info['sub']
            email = user_info['email']
            given_name = user_info.get('given_name', '')
            family_name = user_info.get('family_name', '')

            # Check if player with given sub exists
            try:
                player = Player.objects.get(username=sub)
            except Player.DoesNotExist:
                # Create player with user info
                player = Player.objects.create(
                    username=sub,
                    email=email,
                    first_name=given_name,
                    last_name=family_name,
                )
            
            # Authenticate user and login
            user = player.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect("index")
    else:
        return HttpResponse("Failed to retrieve user info")
    
    return redirect('index')


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )

def index(request):
    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )