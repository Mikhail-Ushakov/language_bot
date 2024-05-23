from django.shortcuts import render
from rest_framework import generics
from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteApiView(generics.ListCreateAPIView):
    model = Favorite
    serializer_class = FavoriteSerializer


    def get_queryset(self):
        user = self.request.headers.get('id')
        return Favorite.objects.filter(user=user)
    