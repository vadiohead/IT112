from rest_framework import serializers
from .models import SongList

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongList
        fields = ['id', 'title', 'album', 'year', 'video']