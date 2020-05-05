from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import (
    ValidationError, PermissionDenied
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import (
    League, Team
)
from .serializers import (
    LeagueSerializer, TeamSerializer
)

class LeagueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = League.objects.all().filter(owner=self.request.user)
        return queryset

    serializer_class = LeagueSerializer

    def create(self, request, *args, **kwargs):
        league = League.objects.filter(
            name=request.data.get('name'),
            owner=request.user
        )
        if league:
            msg = 'Created with that name already exists'
            raise ValidationError(msg)
        return super().create(request)

    def destroy(self, request, *args, **kwargs):
        league = League.objects.get(pk=self.kwargs["pk"])
        if not request.user == league.owner:
            raise PermissionDenied("You can't delete this category")
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LeagueTeams(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.kwargs.get('league_pk'):
            league = League.objects.get(pk=self.kwarg["pk"])
            queryset = Team.objects.filter(
                owner=self.request.user,
                league=league
            )
        return queryset

    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SingleLeagueTeam(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.kwargs.get("league_pk") and self.kwargs.get("pk"):
            league = League.objects.get(pk=self.kwargs["league_pk"])
            queryset = Team.objects.filter(
                pk=self.kwargs["pk"],
                owner=self.request.user,
                league=league
            )
        return queryset
    serializer_class = TeamSerializer

class TeamsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Team.objects.all().filter(owner=self.request.user)
        return queryset
    serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied(
                "Only logged in users with accounts can create teams"
            )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        team = Team.objects.get(pk=self.kwargs["pk"])
        if not request.user == team.owner:
            raise PermissionDenied("You can't delete this team")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        team = Team.objects.get(pk=self.kwargs["pk"])
        if not request.user == team.owner:
            raise PermissionDenied("Ypu can't update this team")
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
