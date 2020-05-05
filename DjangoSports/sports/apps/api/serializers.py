from rest_framework import serializers

from apps.api.models import (
    League, Team
)

class TeamSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Team
        fields = ('id', 'name', 'conference',
                  'division', 'owner', 'league',
                  'created_at', 'updated_at', 'is_public')

class LeagueSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    teams = TeamSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = League
        fields = ('id', 'name', 'owner', 'description',
                  'teams', 'created_at', 'updated_at')
