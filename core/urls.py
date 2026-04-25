from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FieldViewSet, FieldUpdateViewSet, CustomLoginView, UserViewSet

router = DefaultRouter()
router.register(r'fields', FieldViewSet, basename='field')
router.register(r'updates', FieldUpdateViewSet, basename='fieldupdate')
router.register(r'users', UserViewSet, basename='user') # <-- NEW!

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomLoginView.as_view(), name='login'),
]