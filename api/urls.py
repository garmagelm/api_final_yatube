from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

v1_router = DefaultRouter()
v1_router.register(r'posts', PostViewSet, basename='posts')
v1_router.register(
    r'^posts/(?P<id>\d+)/comments', CommentViewSet, basename='comments')
v1_router.register(r'follow', FollowViewSet, basename='follows')
v1_router.register(r'group', GroupViewSet, basename='groups')

urlpatterns = v1_router.urls

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path(
        'v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'),
]
