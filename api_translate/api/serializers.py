from rest_framework.serializers import ModelSerializer
from .models import Favorite


class FavoriteSerializer(ModelSerializer):
    
    class Meta:
        model = Favorite
        fields = ['user', 'text_from', 'text_to', 'status']


