from rest_framework import serializers
from .models import Review

class ReviewListSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_nickname', 'movie', 'movie_title',
                  'title', 'rating', 'like_count', 'comment_count', 'created_at']

class ReviewDetailSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_nickname', 'movie', 'movie_title',
                  'title', 'content', 'rating',
                  'like_count', 'comment_count',
                  'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, attrs):
        user = self.context['request'].user
        movie = attrs.get('movie')
        if self.instance is None and movie:
            if Review.objects.filter(user=user, movie=movie).exists():
                raise serializers.ValidationError("이미 이 영화에 리뷰를 작성하셨습니다.")
        return attrs
