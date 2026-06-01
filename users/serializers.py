from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg
from .models import User

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'created_at',
                  'review_count', 'average_rating']
        read_only_fields = ['id', 'username', 'created_at']

    def get_review_count(self, obj):
        """사용자가 작성한 리뷰 수"""
        return obj.reviews.count()

    def get_average_rating(self, obj):
        """사용자가 부여한 평균 평점"""
        avg = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg else 0
