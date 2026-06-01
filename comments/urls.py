from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, LikeToggleView

router = DefaultRouter()
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('reviews/<int:review_id>/like/', LikeToggleView.as_view()),
] + router.urls
