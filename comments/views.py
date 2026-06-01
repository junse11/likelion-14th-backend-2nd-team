from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Comment, Like
from .serializers import CommentSerializer
from reviews.models import Review
from reviews.permissions import IsOwnerOrReadOnly

class CommentViewSet(viewsets.ModelViewSet):
    """
    댓글 CRUD API

    - list: 전체 댓글 목록 (review 파라미터로 특정 리뷰의 댓글 필터링 가능)
    - create: 댓글 작성 (로그인 필요)
    - retrieve: 댓글 상세 조회
    - update/partial_update: 댓글 수정 (작성자만)
    - destroy: 댓글 삭제 (작성자만)

    쿼리 파라미터: ?review=<review_id>로 특정 리뷰의 댓글만 조회
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.select_related('user', 'review')
        review_id = self.request.query_params.get('review')
        if review_id:
            qs = qs.filter(review_id=review_id)
        return qs

    def perform_create(self, serializer):
        """댓글 작성 시 현재 로그인 사용자를 자동으로 author로 설정"""
        serializer.save(user=self.request.user)

class LikeToggleView(APIView):
    """
    리뷰 좋아요 토글 API

    POST 요청 시:
    - 좋아요를 누르지 않은 상태 → 좋아요 추가 (201 Created)
    - 이미 좋아요를 누른 상태 → 좋아요 취소 (200 OK)

    응답에 liked(bool)와 like_count(int)가 포함됩니다.
    인증 필요: JWT 토큰
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            review=review
        )
        if not created:
            like.delete()
            return Response(
                {'liked': False, 'like_count': review.likes.count()},
                status=status.HTTP_200_OK
            )
        return Response(
            {'liked': True, 'like_count': review.likes.count()},
            status=status.HTTP_201_CREATED
        )
