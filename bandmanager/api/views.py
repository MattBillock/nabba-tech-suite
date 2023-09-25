import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

from rest_framework import viewsets
from .serializers import PersonSerializer, EmailPreferenceSerializer, SectionSerializer, BandSerializer, CommentarySerializer, \
      VolunteerSerializer, ScoreSerializer, MusicSerializer, ScoreSerializer, PurchasesSerializer, VenueSerializer, \
        PerformanceSlotSerializer, JudgeSerializer, ContestSerializer, MusicianSerializer, DirectorSerializer, EnsembleSerializer
from .models import Person, EmailPreference, Section, Band, Commentary, Volunteer, Score, Music, \
        Score, Purchases, Venue, PerformanceSlot, Judge, Contest, Musician, Director, Ensemble

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
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))

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


class PersonView(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

class EmailPreferenceView(viewsets.ModelViewSet):
    serializer_class = EmailPreferenceSerializer
    queryset = EmailPreference.objects.all()

class SectionView(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()

class BandView(viewsets.ModelViewSet):
    serializer_class = BandSerializer
    queryset = Band.objects.all()

class CommentaryView(viewsets.ModelViewSet):
    serializer_class = CommentarySerializer
    queryset = Commentary.objects.all()

class VolunteerView(viewsets.ModelViewSet):
    serializer_class = VolunteerSerializer
    queryset = Volunteer.objects.all()

class ScoreView(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    queryset = Score.objects.all()

class MusicView(viewsets.ModelViewSet):
    serializer_class = MusicSerializer
    queryset = Music.objects.all()

class PurchasesView(viewsets.ModelViewSet):
    serializer_class = PurchasesSerializer
    queryset = Purchases.objects.all()

class VenueView(viewsets.ModelViewSet):
    serializer_class = VenueSerializer
    queryset = Venue.objects.all()

class PerformanceSlotView(viewsets.ModelViewSet):
    serializer_class = PerformanceSlotSerializer
    queryset = PerformanceSlot.objects.all()

class JudgeView(viewsets.ModelViewSet):
    serializer_class = JudgeSerializer
    queryset = Judge.objects.all()

class ContestView(viewsets.ModelViewSet):
    serializer_class = ContestSerializer
    queryset = Contest.objects.all()

class MusicianView(viewsets.ModelViewSet):
    serializer_class = MusicianSerializer
    queryset = Musician.objects.all()

class DirectorView(viewsets.ModelViewSet):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()

class EnsembleView(viewsets.ModelViewSet):
    serializer_class = EnsembleSerializer
    queryset = Ensemble.objects.all()
