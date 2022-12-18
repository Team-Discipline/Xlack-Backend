from rest_framework.routers import DefaultRouter

from user_profile import views

router = DefaultRouter()

router.register('', views.UserProfileViewSet, basename='UserProfile')
router.register('user_id', views.UserProfileUpdateDeleteViewSet)

urlpatterns = router.urls
