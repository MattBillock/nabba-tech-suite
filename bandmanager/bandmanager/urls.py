"""
URL configuration for bandmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'people', views.PersonView)
router.register(r'email_preferences', views.EmailPreferenceView)
router.register(r'sections', views.SectionView)
router.register(r'bands', views.BandView)
router.register(r'commentaries', views.CommentaryView)
router.register(r'volunteers', views.VolunteerView)
router.register(r'scores', views.ScoreView)
router.register(r'music', views.MusicView)
router.register(r'purchases', views.PurchasesView)
router.register(r'venues', views.VenueView)
router.register(r'performance_slots', views.PerformanceSlotView)
router.register(r'judges', views.JudgeView)
router.register(r'contests', views.ContestView)
router.register(r'musicians', views.MusicianView)
router.register(r'directors', views.DirectorView)
router.register(r'ensembles', views.EnsembleView)
router.register(r'partners', views.PartnerView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path('api/', include(router.urls)),
]

