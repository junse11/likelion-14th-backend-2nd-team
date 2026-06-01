from rest_framework import serializers
from django.db.models import Avg, Count
from .models import Movie

class MovieListSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'director', 'genre', 'release_year',
                  'poster_url', 'average_rating', 'review_count']

class MovieDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_average_rating(self, obj):
        result = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(result, 1) if result else 0

    def get_review_count(self, obj):
        return obj.reviews.count()
