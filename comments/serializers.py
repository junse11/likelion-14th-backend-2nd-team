from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_nickname', 'review', 'content',
                  'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
