from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import (
    LeagueViewSet, LeagueTeams,
    SingleLeagueTeam, TeamsViewSet
)

router = DefaultRouter()
router.register('leagues', LeagueViewSet, basename='leagues')
router.register('teams', TeamsViewSet, basename='teams')

custom_urlpatterns = [
    url(r'leagues/(?P<league_pk>\d+)/teams$', LeagueTeams.as_view, name='league_teams'),
    url(r'leagues/(?P<league_pk>\d+)/teams/(?P<pk>\d+)$', SingleLeagueTeam.as_view, name='single_league_team'),
]

urlpatterns = router.urls
urlpatterns += custom_urlpatterns