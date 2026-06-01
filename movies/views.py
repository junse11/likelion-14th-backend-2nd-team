from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer

class MovieViewSet(viewsets.ModelViewSet):
    """
    영화 정보 CRUD API

    - list: 전체 영화 목록 (검색, 필터링, 정렬, 페이지네이션)
    - create: 영화 등록 (관리자만)
    - retrieve: 영화 상세 조회
    - update/partial_update: 영화 정보 수정 (관리자만)
    - destroy: 영화 삭제 (관리자만)

    필터링: genre, release_year
    검색: title, director
    정렬: release_year, created_at
    """
    queryset = Movie.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'release_year']
    search_fields = ['title', 'director']
    ordering_fields = ['release_year', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer

    def get_queryset(self):
        qs = Movie.objects.all()
        if self.action == 'list':
            qs = qs.annotate(
                average_rating=Avg('reviews__rating'),
                review_count=Count('reviews')
            )
        return qs

    def get_permissions(self):
        """목록/상세/인기/통계 조회는 누구나, 생성/수정/삭제는 관리자만"""
        if self.action in ['list', 'retrieve', 'popular', 'stats']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        인기 영화 TOP 10

        리뷰 수가 많은 순서대로 상위 10개 영화를 반환합니다.
        각 영화의 평균 평점과 리뷰 수가 포함됩니다.
        """
        movies = Movie.objects.annotate(
            review_count=Count('reviews'),
            average_rating=Avg('reviews__rating')
        ).order_by('-review_count')[:10]
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        영화 통계 API

        전체 영화 수, 장르별 영화 수, 전체 평균 평점,
        가장 높은 평점 영화 등의 통계를 반환합니다.
        """
        from reviews.models import Review

        total_movies = Movie.objects.count()
        total_reviews = Review.objects.count()
        overall_avg = Review.objects.aggregate(avg=Avg('rating'))['avg']

        # 장르별 영화 수
        genre_stats = list(
            Movie.objects.values('genre')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # 평점 TOP 5 영화
        top_rated = list(
            Movie.objects.annotate(
                avg_rating=Avg('reviews__rating'),
                review_count=Count('reviews')
            ).filter(review_count__gte=1)
            .order_by('-avg_rating')[:5]
            .values('id', 'title', 'avg_rating', 'review_count')
        )

        return Response({
            'total_movies': total_movies,
            'total_reviews': total_reviews,
            'overall_average_rating': round(overall_avg, 2) if overall_avg else 0,
            'genre_distribution': genre_stats,
            'top_rated_movies': top_rated,
        })
