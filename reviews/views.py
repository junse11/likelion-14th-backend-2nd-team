from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewListSerializer, ReviewDetailSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action

class ReviewViewSet(viewsets.ModelViewSet):
    """
    영화 리뷰 CRUD API

    - list: 전체 리뷰 목록 (페이지네이션, 필터링, 정렬 지원)
    - create: 리뷰 작성 (로그인 필요)
    - retrieve: 리뷰 상세 조회
    - update/partial_update: 리뷰 수정 (작성자만)
    - destroy: 리뷰 삭제 (작성자만)

    필터링: movie, user, rating
    검색: title, content
    정렬: created_at, rating (기본: 최신순)
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['movie', 'user', 'rating']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        return ReviewDetailSerializer

    def get_queryset(self):
        return Review.objects.select_related('user', 'movie').annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )

    def perform_create(self, serializer):
        """리뷰 작성 시 현재 로그인 사용자를 자동으로 author로 설정"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my(self, request):
        """
        내가 작성한 리뷰 목록

        로그인한 사용자 본인이 작성한 리뷰만 필터링하여 반환합니다.
        페이지네이션이 적용됩니다.
        """
        queryset = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReviewListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ReviewListSerializer(queryset, many=True)
        return Response(serializer.data)
